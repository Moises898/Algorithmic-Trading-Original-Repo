import pandas as pd
from Classes.data_operations import *
from time import sleep
import customtkinter
from datetime import date
from random import randint
from Classes.randomForest import inputs_for_random_forest,get_prediction,inputs_for_random_forest_v2
from threading import Timer

# Parameteters for strategy (not modify)
PARAMETERS = lambda x: {    
        "OFFSET": 2,
        "CHOP_LIMIT": 50.24,
        "CHOP_LENGHT": 4,
        "ATR_LENGHT": 15,
        "FACTOR": 2.4,
        "EMA_OPEN": 4 if x == "XAUUSD" else 2,
        "EMA_LH": 2
    }

# DEFAULT CUSTOM PARAMETERS
TARGET_POINTS_EURUSD = 65
TARGET_POINTS_XAUUSD = 800
RISK = .0025
PROFIT = .0035
ENTRIES_PER_SIGNAL = 4



def positions_open(conn,s=None):
    """
    --Helper Function--    
        Check if exists positions opened in the symbol
    """    
    return not conn.get_positions(0).empty if s is None else not conn.get_positions(0,s=s).empty

def export_signals(df,result,order,reverse,points,symbol,date_for_df,i):    
    """
        Save the parameters from the signals generated to export later
    """
    df["result"] = result
    df["reverse"] = reverse
    df["points"] = points
    df["symbol"] = symbol
    df["order"] = order
    id_rand = randint(1,100)
    df["ID"] = symbol+"-"+date_for_df+"-"+str(points)+"live"+"-"+str(i)+str(id_rand)
    return df,id_rand

def single_trade_open(object,conn,symbol_to_trade,partial_close,risk,target_profit,entries_per_trade,max_trades,timeFrame,flag_session,flag_position,points,lots,both_directions=False,dynamic_sl=True,randomForest=False,fibonacci=False,version_rf=None):
    """
        Strategy execute one trade an analyze when to close it, allows the user play around with different parameters.
            - Automatic Points based on Fibonnaci Levels
            - Trailling Stop
            - Partial Close
            - Random Forest
    """
    point = mt5.symbol_info(symbol_to_trade).point   
    trades = 0
    points_value = 0
    TRADES_SIGNALS = []    
    id = 0
    date_for_df = str(date.today())
    fibonacci_depth = 10
    fibonacci_levels = dict()    
    max_profit_trades = int(.6 * max_trades) if max_trades != 1 else 1
    max_loss_trades = int(.4 * max_trades) if max_trades > 2 else 1
    total_profit = 0
    positive = 0
    negative = 0        
    balance = conn.account_details().balance   
    last_balance = balance
    check_balance = False  
    risk = (balance * risk) * -1
    target_profit = balance * target_profit
    while not flag_session.is_set():        
        # Position Opened
        if positions_open(conn,symbol_to_trade) and not flag_position.is_set():
            if fibonacci:
                # TRAILLING STOP based onf fibonacci levels
                TRAILLING_STOP_FIBONACCI(s=symbol_to_trade,
                                         order=entry,
                                         tickets=tickets_copy,
                                         conn=conn,
                                         levels=fibonacci_levels,
                                         profit=target_profit,
                                         risk=risk,
                                         pnl=total_profit,
                                         flag_to_stop=flag_position,
                                         partial_close=partial_close,
                                         dynamic_sl=dynamic_sl)
            elif dynamic_sl:
                # Active Trailling STOP with 33 %  - Apply in both directions based on entry    
                TRAILLING_STOP(conn=conn,
                            s=symbol_to_trade,
                            order=entry,
                            tickets=tickets_copy,
                            points=points / 3,
                            profit=target_profit,
                            risk=risk,
                            partial_close=partial_close,
                            apply_both_directions=both_directions,
                            flag_to_stop=flag_position,dynamic_sl=dynamic_sl,
                            pnl = total_profit
                            )            
            check_balance = True                                   
        # If operations are alive and flag is set up to True close all positions
        if positions_open(conn,symbol_to_trade) and flag_position.is_set():  
            tickets_to_close = conn.get_positions().ticket.values          
            print(f"Next Trades wil be closed due flag change: {tickets_to_close}")
            for ticket in tickets_to_close:                
                conn.close_position(symbol_to_trade, ticket, entry, lots, comment="Closed by limit reached")                
            check_balance = True
            # Clear the flag to avoid close the next entries
            flag_position.clear()                           
                                             
        # Update current balance        
        if check_balance and last_balance != conn.account_details().equity:            
            profit = conn.account_details().equity - last_balance            
            result = "WIN"
            id += 1
            # Keep tracks of profit/loss operations
            if profit > 0:
                positive += 1                        
            else:
                result = "LOSS"
                negative += 1                
            total_profit += profit
            last_balance = conn.account_details().equity
            check_balance = False            
            if fibonacci:    
                df,id = export_signals(M1,result,entry,False,int(points_value),symbol_to_trade,date_for_df,id)                                            
                TRADES_SIGNALS.append(df) 
            else:
                df,id = export_signals(M1,result,entry,False,points,symbol_to_trade,date_for_df,id)
                TRADES_SIGNALS.append(df)         
        # Close the session if profit/loss or max entries was reached
        if (total_profit >= target_profit) or (total_profit <= risk):
            print(f"The session was closed automatically by {'loss' if total_profit < 0 else 'profit'} limit reached!")
            break
        if (positive == max_profit_trades) or (negative == max_loss_trades) or (negative + positive >= max_trades):
            print("Maximun trades reached")
            break
        if (trades >= max_trades):
            while positions_open(conn,s=symbol_to_trade):                
                print("Waiting until trades closes")
                sleep(60)
        try:            
            M1 = conn.get_data(symbol_to_trade, timeFrame, 100)
        except Exception as e:
            print("Data range failed:", e)
            break
        # Avoid open positions when the profit/risk was acheived
        if (total_profit <= target_profit) or (total_profit >= risk):
            # Open positions if the stratgy detects entries            
            position, entry = EMA_CROSSING(df=M1,offset= PARAMETERS(symbol_to_trade)["OFFSET"], ema_open=PARAMETERS(symbol_to_trade)["EMA_OPEN"],ema_period= PARAMETERS(symbol_to_trade)["EMA_LH"],reverse=True)  
            if randomForest:
                data = inputs_for_random_forest_v2(M1,symbol_to_trade,points_value)  
                entry_from_model = get_prediction(data,'predict_entries_model')      
                # If the random forest was enabled compare the signals          
                if entry != 2 and entry_from_model != entry:  
                    # Determine the entry by a trendline by the same depth from the fibonacci
                    trend = Technical(M1).calculate_trend_by_bars_trend(-fibonacci_depth) #TREND_BY_TRENDLINE(fibonacci_depth)  
                    if trend == entry:
                        print(f"Normal entry will be opened {entry}")
                    else:      
                        print("Entry will be reversed: ", entry," -> ", entry_from_model)
                        entry = entry_from_model
            if position:                     
                lowest,highest = Technical(M1).get_lowest_and_highest(fibonacci_depth) 
                difference = abs(highest - lowest)
                fibonacci_levels = {
                    11.2: .112*difference,
                    23.6: .236 * difference,
                    38.2: .382 * difference,        
                    50: .5 * difference,
                    61.8: .618 * difference
                }                            
                if entry == 1:
                    print("****************** BUY ******************")
                    decimal_places = len(str(mt5.symbol_info_tick(symbol_to_trade).ask).split(".")[1])
                    entry_price = mt5.symbol_info_tick(symbol_to_trade).ask
                    sl = round(entry_price - fibonacci_levels[23.6], decimal_places)
                    tp = round(entry_price + fibonacci_levels[61.8], decimal_places)
                else:
                    print("****************** SELL ******************")   
                    decimal_places = len(str(mt5.symbol_info_tick(symbol_to_trade).bid).split(".")[1])
                    entry_price = mt5.symbol_info_tick(symbol_to_trade).bid
                    sl = round(entry_price + fibonacci_levels[23.6], decimal_places)
                    tp = round(entry_price - fibonacci_levels[61.8], decimal_places)   
                    points_value = int((max([tp,entry_price]) - min([tp,entry_price])) * (100 if symbol_to_trade == "XAUUSD" else 100_000))                                                                             
                tickets = [] 
                tickets_copy = []                 
                if fibonacci and points_value < 60 and symbol_to_trade == "XAUUSD":
                        print("Position will be skipped")
                        position = False                                                                                 
                else:
                    while len(tickets) < entries_per_trade:                    
                        # Set SL and TP based in Fibonacci levels
                        if fibonacci and symbol_to_trade == "XAUUSD":                            
                            object.points = str(points_value)
                            ticket = conn.open_position(symbol_to_trade, entry, lots,[sl,tp])
                        # Set  SL and TP with user inputs
                        else:
                            ticket = conn.open_position(symbol_to_trade, entry, lots,points)
                        if ticket != 0:
                            tickets.append(ticket) 
                    valid_entries = False
                    for ticket in tickets:
                        if ticket != 10019:
                            valid_entries = True
                            tickets_copy.append(ticket)                        
                    if not valid_entries:
                        flag_session.set()
                        print("Please reduce the lots")                                    
        sleep(1)
    # Make sure to close all trades before close the session
    if positions_open(conn,s=symbol_to_trade):        
        tickets_to_close = conn.get_positions().ticket.values          
        print(f"Next Trades wil be closed before close the session: {tickets_to_close}")
        for ticket in tickets_to_close:                
            conn.close_position(symbol_to_trade, ticket, entry, lots, comment="Closed by limit reached")
    if not flag_session.is_set():                  
        flag_session.set()
    # Display the buttons when session is closed automatically by one condtion reached
    try:        
        object.main_frame.stop_thread.grid_forget()    
        object.main_frame.close_trades.grid_forget()                
        object.sidebar_button_2.configure(state="enabled")
        object.main_frame.stop_thread = customtkinter.CTkButton(object.main_frame, text="Return Strategy Screen",command= object.start_connection)
        object.main_frame.stop_thread.grid(row=7, column=0,columnspan=2, padx=40, pady=0,sticky="ew")                             
    except:
        pass
    # Export the current operations
    print(f"Profit: {total_profit}")  
    if len(TRADES_SIGNALS) > 0:
        if fibonacci:                
            pd.concat(TRADES_SIGNALS).to_csv(fr"C:\Users\Moy\Documents\Python\Algorithmic Trading\HFT\backtest_data\{symbol_to_trade}-{date_for_df}-{points_value}-fibonacci-{id}.csv")     
        else:
            pd.concat(TRADES_SIGNALS).to_csv(fr"C:\Users\Moy\Documents\Python\Algorithmic Trading\HFT\backtest_data\{symbol_to_trade}-{date_for_df}-{points}-{id}.csv")     

def EMA_CROSSING(df,offset=3, ema_open=15, ema_period=3,reverse=False,volume_filter=False,show=False):
    """
    Description:
        The strategy looks for crossing between the upper and lower EMA with the central one. 
        - CHOP Index < 50.
        - Supertrend Direction is opposite to the signal detected by EMA Crossing.
        - Trend of last 30 times is at least 35 % of signal detected. If not open in main trend     
    Additional:
        - Volume Filter: Volume increase from previous bar. (If not signal skipped)       

    Args:
        df (pandas dataframe): Data used to check for entries
        offset (int, optional): _description_. Defaults to 3.
        ema_open (int, optional): _description_. Defaults to 15.
        ema_period (int, optional): _description_. Defaults to 3.
        reverse (bool, optional): _description_. Defaults to False.
        volume_filter (bool, optional): Extra Filter, If volume don't increase signal turns to False . Defaults to False.
        show (bool, optional): Display signal detected to the console. Defaults to False.

    Returns:
        list --> boolean,int: Returns TRUE or FALSE and the trend to open trade
    """
    
    operation = False
    trend_for_operation = 2
    M1_technical = Technical(df)
    series_bar = M1_technical.get_bars_direction(30)
    counters = bar_trend_ocurrencies(series_bar)
    if len(counters) > 2:
        total = 30 - counters[2]
    else:
        total = 30    
    if M1_technical.calculate_chopiness_index(PARAMETERS("XAUUSD")["CHOP_LENGHT"])[-1] < PARAMETERS("XAUUSD")["CHOP_LIMIT"]:                
        # Set PARAMETERS         
        EMA_LOW = M1_technical.EMA(entry="low", period=ema_period, deviation=offset)
        EMA_HIGH = M1_technical.EMA(entry="high", period=ema_period, deviation=offset)
        EMA_OPEN = M1_technical.EMA(entry="open", period=ema_open, deviation=-1)
        supertrend = M1_technical.calculate_super_trend(PARAMETERS("XAUUSD")["ATR_LENGHT"], PARAMETERS("XAUUSD")["FACTOR"])          
        if (CROSSING(EMA_OPEN, EMA_HIGH, 0)) and supertrend == 1:            
            # SELL Under
            if counters[-1] / total >= .35:
                if show:
                    print("Sell under")
                operation = True
                trend_for_operation = 0                
            else:
                if show:
                    print("Buy by Strong Trend")
                operation = True
                trend_for_operation = 1                 
        
        elif (CROSSING(EMA_OPEN, EMA_LOW, 1)) and supertrend == 0:
            # BUY Over
            if counters[1] / total >= .35:
                if show:
                    print("Buy over")
                operation = True
                trend_for_operation = 1
            else:
                if show:
                    print("Sell by Strong Trend")
                operation = True
                trend_for_operation = 0                
        if operation and volume_filter:
            if df.tick_volume.iloc[-1] < df.tick_volume.iloc[-2]:                
                operation = False
        if reverse:
            trend_for_operation = 0 if trend_for_operation == 1 else 1
    return operation, trend_for_operation
