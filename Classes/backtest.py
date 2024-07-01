from Classes.data_operations import *
from Classes.Strategies import *
import numpy as np
from Classes.randomForest import *
from lightweight_charts import Chart

DEFAULT_RANGE = lambda x:  range(100, 1200, 100) if x == "XAUUSD" else range(40, 100, 5)

def backtest_strategy(conn,n_periods,symbol,reverse,points,apply_volume_filter=False,candles_per_entry=10,fibonacci=False,model=False,dataFrame=None):
    """
        Backtest the strategy to detect entries in the past, the method will return a dictionary with the entry price and the operation type (BUY/SELL)
    """
    FINAL_EMA_OPEN = EMA_OPEN_XAUUSD if symbol == "XAUUSD" else EMA_OPEN_EURUSD
    FINAL_EMA_LH = EMA_LH_XAUUSD if symbol == "XAUUSD" else EMA_LH_EURUSD
    candles_lenght = n_periods * 2
    if dataFrame is None:
        df_testing = conn.data_range(symbol,"M1",candles_lenght)
        # Emulate Live Trading 
        start = n_periods + 1
        iterations = n_periods
    else:
        if dataFrame.shape[0] >= 200:
            df_testing = dataFrame
            start = 101
            iterations = (dataFrame.shape[0] - start)
    df_testing[["Sell","Buy","SL","TP","SL1","TP1"]] = np.nan
    adjusted_points = points * mt5.symbol_info(symbol).point   
    final_points = points 
    operations = {}        
    open_prices = df_testing['open'].values
    # Emulate Live Trading     
    index_to_continue = 0   
    trade_open = False
    for i in range(iterations):        
        df_for_strategy = df_testing.iloc[start-100:start]                             
        # Simulate entries
        position, entry = EMA_CROSSING(df=df_for_strategy,offset= OFFSET, ema_open=FINAL_EMA_OPEN,ema_period= FINAL_EMA_LH,reverse=reverse,volume_filter=apply_volume_filter,show=False)                                                                           
        if position and not trade_open:              
            ####
            flag_randomForest = False            
            while True:
                # Update the value where signal is generated 
                if entry == 0:
                    column = "Sell"
                else:
                    column = "Buy"
                # Entry price
                prices = df_testing[column].values  
                prices[start] = open_prices[start]
                df_testing[column] = prices 
                # Calculate SL and TP
                if fibonacci:
                    lowest,highest = Technical(df_for_strategy).LOWEST_AND_HIGHEST(10) 
                    #decimal_places = len(str(lowest).split(".")[1])
                    difference = abs(highest - lowest)
                    fibonacci_levels = {
                        23.6: .236 * difference,
                        38.2: .382 * difference,
                        50: .5 * difference,
                        61.8: .618 * difference
                    }                                
                    if entry == 1:                                                        
                        sl = prices[start] - fibonacci_levels[23.6]
                        tp1 = prices[start] + fibonacci_levels[50]
                        tp = prices[start] + fibonacci_levels[61.8]                     
                    else:                    
                        sl = prices[start] + fibonacci_levels[23.6]
                        tp1 = prices[start] - fibonacci_levels[50]
                        tp = prices[start] - fibonacci_levels[61.8]                                    
                else:
                    sl = df_testing["SL"].values              
                    tp  = df_testing["TP"].values                    
                    sl = prices[start] - adjusted_points if entry == 1 else prices[start] + adjusted_points
                    tp = prices[start] + adjusted_points if entry == 1 else prices[start] - adjusted_points    
                points_value = int((max([tp,prices[start]]) - min([tp,prices[start]])) * (100 if symbol == "XAUUSD" else 100_000))                
                sl_value = abs(int((max([sl,prices[start]]) - min([sl,prices[start]])) * (100 if symbol == "XAUUSD" else 100_000)))
                # Use the model to check entries reversed
                if model and not flag_randomForest:
                    data = inputs_for_random_forest(df_for_strategy,entry,symbol,points_value)  
                    prediction =  get_prediction(data)
                    if prediction:
                        entry = 0 if entry == 1 else 1 
                    flag_randomForest = True                                             
                else:
                    break
            ####                             
            index_to_continue = i + candles_per_entry
            trade_open = True                                                    
            # Add SL and TP to the DF
            df_testing["SL"] = sl
            df_testing["TP"] = tp                       
            # Strategy        
            df_for_strategy["SL"] = sl
            df_for_strategy["TP"] = tp            
            df_to_plot = df_testing.iloc[start:] 
            if fibonacci and (points_value < 100 and symbol == "XAUUSD") or (points_value < 35 and symbol == "EURUSD"):
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
        # When the loop iterate over candles_per_entry - 1 bars strategy will open new trades again
        elif i == index_to_continue - 1:
            trade_open = False
        start += 1
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

# Execute the method above to get the best parameters
def optimize_strategy(conn, n_periods, symbol):
    """
    Optimize the strategy by testing different points for SL and TP or by automatic Points using Fibonacci levels

    Args:
        conn: Database connection or data source.
        n_periods: Number of periods for backtesting.
        symbol: The trading symbol.

    Returns:
        A dictionary with the best SL and TP points, the best result, and whether reversing the entries and/or using
        the volume filter is better.
    """

    best_result = None
    best_points = None    
    points_range = DEFAULT_RANGE(symbol)
    results = []   
    fibonnaci_is_best = False
    random_is_best = False
    for points in points_range:  
        # Original Strategy    
        win_rate,_ = backtest_and_analyze(conn, n_periods, symbol, reverse=False, points=points, volume_filter=False,fibonnaci=False, random_forest=False)
        results.append((win_rate, points,False,False))
        # Strategy with random forest
        win_rate,_ = backtest_and_analyze(conn, n_periods, symbol, reverse=False, points=points, volume_filter=False,fibonnaci=False, random_forest=True)
        results.append((win_rate, points,False,True))                                          
                
    # Add results using fibonacci levels
    win_rate, fibonnaci = backtest_and_analyze(conn, n_periods, symbol, reverse=False, points=points, volume_filter=False,fibonnaci=True, random_forest=False)
    results.append((win_rate,fibonnaci,True,False))
    # Add results using fibonacci levels and random forest
    win_rate, fibonnaci2 = backtest_and_analyze(conn, n_periods, symbol, reverse=False, points=points, volume_filter=False,fibonnaci=True, random_forest=False)
    results.append((win_rate,fibonnaci2,True,True))
    
    # Check best results
    for win_rate,points,fibonnaci_implemented,randomForest in results:
        if best_result is None or win_rate > best_result:
            best_result = win_rate
            best_points = points
            fibonnaci_is_best = fibonnaci_implemented
            random_is_best = randomForest
    return {
        "best_points": best_points,
        "best_result": best_result,
        "fibonnaci_used": fibonnaci_is_best,
        "randomForest": random_is_best
    }    
    
def get_orders_from_backtesting(operations,symbol):
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
            #df_to_export["OpenTime"] = df_to_export["OpenTime"].astype('int64') // 10**6 
            #df_to_export["OpenTime"] = df_to_export["OpenTime"].dt.tz_localize('UTC').astype('int64') // 10**6 
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
            #df_to_export["CloseTime"] = df_to_export["CloseTime"].dt.tz_localize('UTC').astype('int64') // 10**6            
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
            
            profit = pips * 0.01 * pip_value
            df_to_export["Pips"] = round(pips,2)
            df_to_export["Profit"] = round(profit,2)
            dfs.append(df_to_export.iloc[0])
    if len(dfs) > 0:
        final_df = pd.DataFrame(dfs)       
        # Rest of columns
        final_df['Size'] = 0.01
        final_df['Comment'] = "ATLAS Backtest"
        final_df['LotSize'] = 100000
        # Calcular la comisión (10 USD por lote estándar)
        commission_per_lot = 10
        final_df['Commission'] = 0.01 * commission_per_lot
        final_df['Swap'] = 0
        
        return final_df[["OpenTime","OrderNumber","Type","Size","Item","OpenPrice","S/L","T/P","CloseTime","ClosePrice","Swap","Pips","Profit","Comment","LotSize","Commission"]]
    else:
        return pd.DataFrame()