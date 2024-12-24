from Classes.Strategies import PARAMETERS,EMA_CROSSING
from Classes.technical import Technical
from Classes.randomForest import inputs_for_random_forest, get_prediction
import pandas as pd
from datetime import date
import MetaTrader5 as mt5
import numpy as np
import math

DEFAULT_RANGE = lambda x:  range(100, 1200, 100) if x == "XAUUSD" else range(40, 100, 5)

def backtest_strategy(conn,n_periods,symbol,reverse,points,interval_entries=10,depth=11,fibonacci=False,model=False,dataFrame=None):
    """
        Backtest the strategy to detect entries in the past, the method will return a dictionary with the entry price and the operation type (BUY/SELL)                
    """    
    start = 100
    operations = {} 
    adjusted_points = points * mt5.symbol_info(symbol).point   
    final_points = points        
    
    if dataFrame is None:        
        candles_lenght = n_periods + 100
        df_testing = conn.get_data(symbol, "M1", candles_lenght)        
        iterations = n_periods
    else:
        if dataFrame.shape[0] < 100:
            print("Rows need to be greater or equal to 100")
            return None,None    
        df_testing = dataFrame            
        iterations = (dataFrame.shape[0] - start)
                
    df_testing[["Sell","Buy","SL","TP","SL1","TP1"]] = np.nan            
    open_prices = df_testing['open'].values
    values_for_strategy = PARAMETERS(symbol)  
    entries = ["Sell", "Buy"]
    # Emulate Live Trading     
    index_to_continue = 0   
    trade_open = False
    for i in range(iterations-1):    
        try:    
            df_for_strategy = df_testing.iloc[start-100:start]                             
            # Simulate entries            
            position, entry = EMA_CROSSING(df=df_for_strategy,offset= values_for_strategy["OFFSET"], ema_open=values_for_strategy["EMA_OPEN"],ema_period=values_for_strategy["EMA_LH"],reverse=reverse,show=False)
            if position and not trade_open:                              
                flag_randomForest = False            
                while True:
                    # Update the value where signal is generated                     
                    column = entries[entry]
                    # Entry price                    
                    df_testing.at[start, column] = open_prices[start]    
                    current_price = df_testing.at[start, column]              
                    # Calculate SL and TP
                    if fibonacci:
                        lowest,highest = Technical(df_for_strategy).get_lowest_and_highest(depth)                     
                        difference = abs(highest - lowest)
                        fibonacci_levels = {
                            23.6: .236 * difference,
                            38.2: .382 * difference,
                            50: .5 * difference,
                            61.8: .618 * difference
                        }                                
                        if entry == 1:                                                        
                            sl = current_price - fibonacci_levels[23.6]                            
                            tp = current_price + fibonacci_levels[61.8]                     
                        else:                    
                            sl = current_price + fibonacci_levels[23.6]                            
                            tp = current_price - fibonacci_levels[61.8]                                    
                    else:
                        decimal_places = len(str(adjusted_points).split(".")[1])
                        sl = df_testing["SL"].values              
                        tp  = df_testing["TP"].values                    
                        sl = round(current_price - (adjusted_points/2),decimal_places) if entry == 1 else round(current_price + (adjusted_points/2),decimal_places)                    
                        tp = current_price + adjusted_points if entry == 1 else current_price - adjusted_points    
                    points_value = int((max([tp,current_price]) - min([tp,current_price])) * (100 if symbol == "XAUUSD" else 100_000))                
                    sl_value = abs(int((max([sl,current_price]) - min([sl,current_price])) * (100 if symbol == "XAUUSD" else 100_000)))
                    # Use the model to check entries reversed
                    if model and not flag_randomForest:
                        data = inputs_for_random_forest(df_for_strategy,entry,symbol,points_value)  
                        prediction =  get_prediction(data)
                        # Reverse the entry if the random forest was enabled and the trend by the bars is equal
                        # If the random forest was enabled compare the signals          
                        if entry != 2 and prediction != entry:  
                            # Determine the entry by a trendline by the same depth from the fibonacci
                            trend = Technical(df_for_strategy).calculate_trend_by_bars_trend(-10) #TREND_BY_TRENDLINE(fibonacci_depth)  
                            if trend != entry:                    
                                entry = 0 if entry == 1 else 1 
                        flag_randomForest = True                                             
                    else:
                        break                                          
                index_to_continue = i + interval_entries
                trade_open = True                                                    
                # Add SL and TP to the DF
                df_testing["SL"] = sl
                df_testing["TP"] = tp                       
                # Strategy        
                df_for_strategy["SL"] = sl
                df_for_strategy["TP"] = tp            
                df_to_plot = df_testing.iloc[start:] 
                if fibonacci and (not (100 <= sl_value <= 500) and symbol == "XAUUSD") or (points_value < 40 and symbol == "EURUSD"):
                        pass
                        #print("Position will be skipped")                   
                else:
                    operations[open_prices[start]] = {
                    "type": "SELL" if entry == 0 else "BUY",               
                    "df": df_to_plot,
                    "df_strategy": df_for_strategy,
                    "reversed": prediction if model else reverse,
                    "points": points_value,
                    "sl_points": sl_value
                        }
                    # Reset the values of the original dataframe to keep just one value per df
                    df_testing[column] = np.nan  
                    df_testing[["SL","TP"]] = np.nan              
            # When the loop iterate over interval_entries - 1 bars strategy will open new trades again
            elif i == index_to_continue - 1:
                trade_open = False
            start += 1
        except IndexError:
            pass
    return operations,final_points

# Analyze and modify entries to analyze later on
def analyze_results(backtest_dictionary,periods=100):
    """
        Analyze the entries to determine how profitable were the entries
    """
    counters = {
        "sl_counter": 0,
        "tp_counter":0
    }             
    trades = {}
    for key in backtest_dictionary.keys():
        df = backtest_dictionary[key]["df"]
        sl_flag = False
        tp_flag = False
        trade_result = None

        for index, row in df.reset_index().iterrows():
            sl = row["SL"]
            tp = row["TP"]

            # Check for SELL type
            if backtest_dictionary[key]["type"] == "SELL":
                if row["high"] >= sl and not sl_flag:
                    counters["sl_counter"] += 1
                    sl_flag = True
                    trade_result = {"result": "LOSS", "df": df[['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']].iloc[index:index + periods]}
                elif row["low"] <= tp and not tp_flag:
                    counters["tp_counter"] += 1
                    tp_flag = True
                    trade_result = {"result": "WIN", "df": df[['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']].iloc[index:index + periods]}

            # Check for BUY type
            else:
                if row["low"] <= sl and not sl_flag:
                    counters["sl_counter"] += 1
                    sl_flag = True
                    trade_result = {"result": "LOSS", "df": df[['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']].iloc[index:index + periods]}
                elif row["high"] >= tp and not tp_flag:
                    counters["tp_counter"] += 1
                    tp_flag = True
                    trade_result = {"result": "WIN", "df": df[['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']].iloc[index:index + periods]}

            if sl_flag or tp_flag:
                trades[key] = trade_result
                break

        # If neither SL nor TP was hit
        if not sl_flag and not tp_flag:
            trade_result = {"result": "OPEN", "df": df[['open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']]}

                                               
            
    return counters,trades   

# Helper fucntion to return only the win rate
def backtest_and_analyze(conn, n_periods, symbol, reverse, points, volume_filter,fibonnaci,random_forest):
    """
    Perform backtest and analyze results.
    Returns:
        The result metric (win rate) of the backtest.
    """
    final_points = points
    backtest_results,points_fibonacci = backtest_strategy(conn, n_periods, symbol, reverse, points, volume_filter,fibonacci=fibonnaci,model=random_forest)
    counters, _ = analyze_results(backtest_results)
    if sum(counters.values()) > 0:
        win_rate = counters["tp_counter"]  / sum(counters.values())
    else:
        win_rate = 0
    if fibonnaci:
        final_points = points_fibonacci
    return win_rate, final_points

def strategy_optimization(conn,symbol,periods=500):
    """    
    This function execute a backtest to optimize the parameters based on a score
    
    Args:
        conn (MT5): MT5 connection object
        symbol (string): Symbol to use for the backtesting
        periods (int): Number of periods to perfom the backtest

    Returns:
        list [depth,reverse]: Returns a list with best pair of values 
    """
    depths = [30,100]
    reverse_entries = [True]
    best_values = []
    best_score = -float('inf') 
    for depth in depths:
        for reverse in reverse_entries:            
            trades, _ = execute_backtest(connection=conn,
                                            symbol=symbol,
                                            n_periods=periods,
                                            points=400,  # best_settings['best_points'],
                                            automatic_points=True,  # best_settings['fibonnaci_used'],
                                            use_random_forest=False,  # best_settings['randomForest'],                                    
                                            reverse_entries=reverse,
                                            depth=depth
                                            )
            if trades:                                
                backtest_results = get_orders_from_backtesting(trades, symbol, lots=0.01)   
                profit = backtest_results["Profit"].sum() - backtest_results["Commission"].sum()
                num_trades = backtest_results.shape[0]                 
                if profit > 0:
                    score = profit * math.log(num_trades+1)
                else:
                    score = profit / (num_trades + 1)                
                if best_score < score:
                    best_score = score
                    best_values = [depth,reverse]   
    return best_values      

def execute_backtest(connection, symbol, n_periods, points=100,depth=11, automatic_points=False, use_random_forest=False,
                    reverse_entries=False,**kwargs):
    dataFrame = kwargs.get("dataFrame",None)        
    # Execute with custom parameters
    operations, _ = backtest_strategy(connection, n_periods, symbol, reverse_entries, points,depth=depth,
                                      fibonacci=automatic_points, model=use_random_forest,dataFrame=dataFrame)
    counters, results = analyze_results(operations)
    try:
        win_rate = counters['tp_counter'] / sum(counters.values())
        drop_open_trades = []
        # Ask the user if want to display the open trades
        for trade in operations.keys():
            if trade in results.keys():
                operations[trade]["result"] = results[trade]["result"]
            else:
                drop_open_trades.append(trade)
                # operations[trade]["result"] = "OPEN"
        # Drop the keys
        for open_trade in drop_open_trades:
            del operations[open_trade]
        return operations, win_rate
    except ZeroDivisionError:
        return None, None

def get_orders_from_backtesting(operations,symbol,lots=0.01):
    counters,trades = analyze_results(operations)
    date_for_df = str(date.today())
    dfs = []    
    for i,key in enumerate(operations.keys()):        
        df = operations[key]["df"]
        df_to_export = df.reset_index()
        df_to_export.rename(columns={"SL":"S/L","TP":"T/P","time":"OpenTime"},inplace=True)                
        if key in trades.keys():                                
            df_to_export["Item"] = symbol
            df_to_export["Type"] = "Sell" if operations[key]["type"] == "SELL" else "Buy"
            df_to_export["OrderNumber"] = i                                                
            df_to_export["OpenPrice"] = df_to_export["open"]                       
            # Get the Close Price and CloseTime
            for idx, (high, low) in enumerate(zip(df["high"], df["low"])):
                if operations[key]["type"] == "BUY":
                    if high >= df_to_export["T/P"].iloc[0] or low <= df_to_export["S/L"].iloc[0]:
                        end = idx
                        break
                else:
                    if low <= df_to_export["T/P"].iloc[0] or high >= df_to_export["S/L"].iloc[0]:
                        end = idx
                        break   
            df_to_export["CloseTime"] = df.reset_index().iloc[end]["time"]            
            df_to_export["ClosePrice"] =  df_to_export["T/P"].iloc[0] if trades[key]["result"] == "WIN" else df_to_export["S/L"].iloc[0]
            # Calculate pips and profit
            if symbol == 'EURUSD':
                # EURUSD: Pips = (Close - Open) * 10000, Valor por pip = 10 USD por lote estándar (1 lote)
                pips = (df_to_export["ClosePrice"]  -  df_to_export["OpenPrice"]) * 10000 if operations[key]["type"] == "BUY" else (df_to_export["OpenPrice"]  -  df_to_export["ClosePrice"]) * 10000
                pip_value = 10
            elif symbol == 'XAUUSD':
                # XAUUSD: Pips = (Close - Open) * 100, Valor por pip = 1 USD por lote estándar (1 lote)
                pips = (df_to_export["ClosePrice"]  -  df_to_export["OpenPrice"]) * 100 if operations[key]["type"] == "BUY" else (df_to_export["OpenPrice"]  -  df_to_export["ClosePrice"]) * 100
                pip_value = 1
            else:
                pips = 0
                pip_value = 0
            
            profit = pips * lots * pip_value
            df_to_export["Pips"] = round(pips,2)
            df_to_export["Profit"] = round(profit,2)
            dfs.append(df_to_export.iloc[0])
    if len(dfs) > 0:
        final_df = pd.DataFrame(dfs)       
        # Rest of columns
        final_df['Size'] = lots
        final_df['Comment'] = "ATLAS Backtest"
        final_df['LotSize'] = 100000
        # Calcular la comisión (10 USD por lote estándar)
        commission_per_lot = 10
        final_df['Commission'] = lots * commission_per_lot
        final_df['Swap'] = 0
        
        return final_df[["OpenTime","OrderNumber","Type","Size","Item","OpenPrice","S/L","T/P","CloseTime","ClosePrice","Swap","Pips","Profit","Comment","LotSize","Commission"]]
    else:
        return pd.DataFrame()