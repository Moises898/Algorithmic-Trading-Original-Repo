from time import sleep
import MetaTrader5 as mt5
from Classes.technical import Technical
from Classes.Strategies import EMA_CROSSING,PARAMETERS
from Classes.randomForest import inputs_for_random_forest_v2,get_prediction
from datetime import datetime,timedelta
import operator

def on_tick(mt5_connection,symbol,strategy,user_parameters):
    """
    Execute the selected strategy with user arg every second to detect entries

    Args:
        mt5_connection (MT5 Class): Object created with the connection to the MT5 server
        symbol (str): Name of the symbol to execute the strategy        
        user_parameters (dict): Dictionary with key values options for Strategy selected
            -profit (float): Target profit for session
            -loss (float): Maximum loss per session
            -max_trades (int): Max number of trades to open per session
            -dynamic_points (boolean): Determine SL / TP automatically.
            -points (int): Set SL / TP based on user parameters
    """    
    
    initial_balance = mt5_connection.account_details().balance
    current_balance = initial_balance
    time_open = None
    position = False
    trades_results = {
        "win": 0,
        "loss": 0
    }
    trades_open = 0
    single = True if strategy == "single" else False
    # Loop until a condition is met
    while True:
        dataFrame = mt5_connection.get_data(symbol,user_parameters["timeFrame"],101)[:-1]     
        # Open one trade at the time
        if strategy == "single":            
            if user_parameters["dynamic_points"]:                  
                current_balance, trades = ema_crossing_dynamic_points(mt5_connection,initial_balance,dataFrame,symbol,single,user_parameters)                
            else:                
                current_balance, trades = ema_crossing_static_points(mt5_connection,initial_balance,dataFrame,symbol,single,user_parameters)                
            trades_results["win"] += trades["win"]
            trades_results["loss"] += trades["loss"]
        # Open multiple trades with intervals
        elif strategy == "multiple":            
            if user_parameters["dynamic_points"]:   
                if trades_open <= user_parameters["max_trades"]:         
                    time_open,trade = ema_crossing_dynamic_points(mt5_connection,initial_balance,dataFrame,symbol,single,user_parameters,time=time_open)
                    if trade:
                        trades_open += 1                
            else:             
                time_open = ema_crossing_static_points(mt5_connection,initial_balance,dataFrame,symbol,single,user_parameters,time=time_open)                        
            
        if check_limits_per_session(mt5_connection,initial_balance,user_parameters["profit"],user_parameters["loss"],trades_results,user_parameters["max_trades"]):
            print("Close")
            break
        sleep(60)

def ema_crossing_dynamic_points(mt5_connection,initial_balance,df,symbol,single,strategy_options,**kwargs):
    """
    Execute Ema Crossing strategy opening one trade at the time and calculate the SL and TP automatically based on fibonacci levels.

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
        initial_balance (float): Initial Balance before start the session
        df (DataFrame): DataFrame to use to check for new entries.
        single (boolean): True if only one trade will be opened at the time
        strategy_options (dict): Dictionary with key values options for Strategy selected
            -entries_per_trade (int): number of entries to open when a signal is detected.
            -lots (float): Size per trade to open when a signal is detected.
            -trailling_stop (boolean): Apply a Trailling stop function to set new SL levels
            -partial_close (boolean): Close one trade when intermediate levels are reached (Requires Trailling Stop Enabled)                   
    
    kwargs:
        -time (datetime): Time when trades can be opened again
    
    Returns:
        position (boolean), last_balance (float), trades_result (dict), time (datetime) : 
            -New balance after trades are closed
            -Result of the trade in key-value pairs.
            -Time when trades can be opened when kwargs are passed
    """
    values_for_strategy = PARAMETERS(symbol)  
    tickets = []       
    trades_result = {"win":0,"loss":0}
    last_balance = initial_balance    
    time_to_open = kwargs.get("time", None)        
    position = False  
    valid_entries = False
    # If there's no open trades, look for entries
    if mt5_connection.get_positions(0).empty or not single:                                    
        position, entry = EMA_CROSSING(df=df,offset=values_for_strategy["OFFSET"], ema_open=values_for_strategy["EMA_OPEN"],ema_period= values_for_strategy["EMA_LH"],reverse=True)                         
        # Check if multiple entries can be opened        
        if not single and time_to_open is not None:
            if datetime.now() <= time_to_open:
                position = False
        if position:                     
                lowest,highest = Technical(df).get_lowest_and_highest(30) 
                difference = abs(highest - lowest)
                fibonacci_levels = {
                    11.2: .112* difference,
                    23.6: .236 * difference,
                    38.2: .382 * difference,        
                    50: .5 * difference,
                    61.8: .618 * difference
                }                            
                if entry == 1:
                    print("****************** BUY ******************")
                    decimal_places = len(str(mt5.symbol_info_tick(symbol).ask).split(".")[1])
                    entry_price = mt5.symbol_info_tick(symbol).ask
                    sl = round(entry_price - fibonacci_levels[23.6], decimal_places)
                    tp = round(entry_price + fibonacci_levels[61.8], decimal_places)
                else:
                    print("****************** SELL ******************")   
                    decimal_places = len(str(mt5.symbol_info_tick(symbol).bid).split(".")[1])
                    entry_price = mt5.symbol_info_tick(symbol).bid
                    sl = round(entry_price + fibonacci_levels[23.6], decimal_places)
                    tp = round(entry_price - fibonacci_levels[61.8], decimal_places)   
                points_to_tp = int((max([tp,entry_price]) - min([tp,entry_price])) * (100 if symbol == "XAUUSD" else 100_000))                                                                                             
                points_to_sl = int((max([sl,entry_price]) - min([sl,entry_price])) * (100 if symbol == "XAUUSD" else 100_000))                                                                                             
                if not (80 <= points_to_sl <= 500) and symbol == "XAUUSD":                    
                    print("Position will be skipped due sl is too short: ",points_to_sl)                                                                                                  
                else:                    
                    # Open trades with SL/TP based on Fibonacci levels
                    while len(tickets) < strategy_options["entries_per_trade"]:                                            
                        ticket = mt5_connection.open_position(symbol, entry, strategy_options["lots"],[sl,tp])                        
                        if ticket != 0:
                            tickets.append(ticket) 
                    valid_entries = False
                    # Check for valid entries
                    for ticket in tickets:
                        if ticket != 10019:
                            valid_entries = True            
                    if not valid_entries:                    
                        print("Please reduce the lots")                                    
                    else:            
                        # If multiple entries is enabled set the time to open trades again            
                        if not single:           
                            # Update time only when the value is None or greater than the last one
                            if time_to_open is None or datetime.now() >= time_to_open:                 
                                time_to_open = datetime.now() + timedelta(minutes=10)                            
                                
    # Apply Trailling Stop to current entries 
    else:
        if strategy_options["trailling_stop"]:
            apply_trailling_stop(mt5_connection,symbol,"fibonacci",strategy_options["partial_close"],profit=strategy_options["profit"],loss=strategy_options["loss"])#,flag_session=strategy_options["flag_session"])        
            # Check results and new balance
            last_balance,trades_result = compare_balance(mt5_connection,last_balance)
    if not single: 
        return time_to_open,valid_entries
    else:
        return last_balance,trades_result
    
def ema_crossing_static_points(mt5_connection,initial_balance,df,symbol,single,strategy_options,**kwargs):
    """
    Execute Ema Crossing strategy opening one trade at the time and applying static SL/TP based on user inputs

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
        initial_balance (float): Initial Balance before start the session
        df (DataFrame): DataFrame to use to check for new entries.
        single (boolean): True if only one trade will be opened at the time
        strategy_options (dict): Dictionary with key values options for Strategy selected
            -entries_per_trade (int): number of entries to open when a signal is detected.
            -lots (float): Size per trade to open when a signal is detected.
            -trailling_stop (boolean): Apply a Trailling stop function to set new SL levels
            -partial_close (boolean): Close one trade when intermediate levels are reached (Requires Trailling Stop Enabled)           
            -points (int): Number of points to set TP, SL is set up using half of points.
        
    kwargs:
        -time (datetime): Time when trades can be opened again
        
    Returns:
    Default:
        position (boolean), last_balance (float), trades_result (dict), time (datetime) : 
            -New balance after trades are closed
            -Result of the trade in key-value pairs.
            -Time when trades can be opened when kwargs are passed
            -True / False if a trade was open
    
            
    """
    values_for_strategy = PARAMETERS(symbol)  
    tickets = []       
    trades_result = {"win":0,"loss":0}
    last_balance = initial_balance      
    time_to_open = 0
    # If there's no open trades, look for entries
    if mt5_connection.get_positions(0).empty:  
        # If a time to open trades is passed,  check time before looking for entries
        if not single and datetime.now() < time_to_open:
            position = False  # Skip this iteration            
        else:
            position, entry = EMA_CROSSING(df=df,offset=values_for_strategy["OFFSET"], ema_open=values_for_strategy["EMA_OPEN"],ema_period= values_for_strategy["EMA_LH"],reverse=True)                                                 
        if position:                                     
            if entry == 1:
                print("****************** BUY ******************")                
            else:
                print("****************** SELL ******************")                  
            # Open trades with SL/TP based on Fibonacci levels
            while len(tickets) < strategy_options["entries_per_trade"]:      
                time_to_open = datetime.now() + timedelta(minutes=10)                                      
                ticket = mt5_connection.open_position(symbol, entry, strategy_options["lots"],strategy_options["points"])                        
                if ticket != 0:
                    tickets.append(ticket) 
            valid_entries = False
            # Check for valid entries
            for ticket in tickets:
                if ticket != 10019:
                    valid_entries = True            
            if not valid_entries:                    
                print("Please reduce the lots")                                    
            else:
                if not single:
                    time_to_open = datetime.now() + timedelta(minutes=10) if time_to_open is None else time_to_open
                
    # Apply Trailling Stop to current entries 
    else:
        if strategy_options["trailling_stop"]:
            apply_trailling_stop(mt5_connection,symbol,"normal",strategy_options["partial_close"],profit=strategy_options["profit"],loss=strategy_options["loss"])#,flag_session=strategy_options["flag_session"])        
            # Check results and new balance
            last_balance,trades_result = compare_balance(mt5_connection,last_balance)
    if not single: 
        return time_to_open,valid_entries
    else:
        return last_balance,trades_result    

def compare_balance(mt5_connection,last_balance):    
    """
    Compare the current balance with the previous one to keep track of results.

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
        last_balance (float): Last balance to compare and determine the result of the last trade.

    Returns:
        current_balance (float): Current new balance.
        trades_result (dict): Result of the trade in key-value pairs.            
    """
    trades_result = {      
        "win": 0,
        "loss": 0
    }
    current_balance = mt5_connection.account_details().equity
    profit = current_balance - last_balance                
    # Keep tracks of profit/loss operations
    if profit > 0:
        trades_result["win"] += 1        
    else:
        trades_result["loss"] += 1                       
    return current_balance,trades_result
            
def check_limits_per_session(mt5_connection,initial_balance,profit,loss,trades,max_trades):
    """
    Close session if one limit is reached is reached

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
        initial_balamce (float): Initial balance to calculate the PnL        
        profit (float): Target profit
        loss (float): Loss configured        
        trades (dict): Trades executed
        max_trades (int): Max number of trades
        single (boolean): Single or Multiple trades mode
    
    Returns:
        boolean: True or False to close the session
    """
    current_balance = mt5_connection.account_details().equity
    pnl = current_balance - initial_balance 
    loss_trades = round(.6 * max_trades,2)
    win_trades = round(.4 * max_trades,2)
    loss = loss * -1 if loss > 0 else loss        
    close_session = False
    if pnl >= profit:
        close_session = True
        print("Profit reached")        
    if pnl <= loss:        
        close_session = True
        print(f"The pnl is {pnl}\nCurrent Balance: {current_balance}\nLoss: {loss}")
        print("Loss reached")
    if mt5_connection.get_positions(0).empty:            
        if trades["win"] >= win_trades:
            close_session = True
            print("Win trades reached")
        if trades["loss"] >= loss_trades:        
            close_session = True
            print("Loss trades reached")
        
    return close_session

def close_trades(mt5_connection):
    """
    Close all the trades trades if exists.

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
    """    
    trades = mt5_connection.get_positions(0)[["symbol", "ticket", "type", "volume"]]   
    if not trades.empty:        
        while True:
            trades_dict = trades.T.to_dict()
            for i in range(len(trades_dict.keys())):
                symbol = trades_dict[i]["symbol"]
                ticket = trades_dict[i]["ticket"]
                order_type = 0 if trades_dict[i]["type"] == 1 else 1                        
                volume = trades_dict[i]["volume"]
            mt5_connection.close_position(symbol, ticket, order_type, volume,"Closing Session")            
            # Check all trades are closed
            trades = mt5_connection.get_positions(0)[["symbol", "ticket", "type", "volume"]]               
            if trades.empty:
                break
            
def apply_trailling_stop(mt5_connection,symbol,trailling_type="normal",partial_close=False,**kwargs):    
    """
    Enable Trailling stop when a trade is open, normal mode is set up by default
        -Normal: Every 30 % of the total distance from entry point to the TP, SL will be adjusted.
        -Fibonnaci: SL is adjusted once the price reach Fibonnacci levels

    Args:
        mt5_connection (MT5 Class): MT5 object to interact with the server
        trailling_type (str, optional): Trailling Stop function. Defaults to "normal".
        partial_close (bool, optional): Close one trade if multiple entries are opend when price reach an intermediate level. Defaults to False.
    
    kwargs:
        profit (float, optional): Close trades if profit is reached. 
        loss (float, optional): Close trades if loss is reached.
        flag_session (boolean, optional): Close trades if flag to close session from the main thread is passed and becomes true.
    
    """
    request_structure = {
            "action": mt5.TRADE_ACTION_SLTP,
            "ticket": None,
            "sl": 0,
            "tp": 0
        }
    trades = mt5_connection.get_positions(0,symbol)[["symbol", "ticket", "type", "volume","sl","tp","price_open"]]   
    trades_dict = trades.T.to_dict()  
    # Take values from first trade  
    open_price,tp,order_type = trades_dict[0]["price_open"], trades_dict[0]["tp"],trades_dict[0]["type"]    
    send_request = False
    decimal_places = len(str(tp).split(".")[1])
    format_values = lambda x: round(x,decimal_places)
     
    # Loop while condition is true
    while not mt5_connection.get_positions(0,symbol).empty:                                                          
        data_m1 =  mt5_connection.get_data(symbol, "M1", 10)
        current_price = data_m1["close"].iloc[-1]                
        if trailling_type == "normal":            
            # Default percentages to use
            percentage_for_tp = .3
            percentage_for_sl = .2
            # Calculate SL value based on TP
            distance_to_tp = max(tp,open_price) - min(tp,open_price)
            tp_level = format_values((open_price + (distance_to_tp * percentage_for_tp)) if order_type == 1 else (open_price + (distance_to_tp * percentage_for_tp))            )
            new_sl = format_values((tp_level - (percentage_for_sl * distance_to_tp)) if order_type == 1 else (tp_level + (percentage_for_sl * distance_to_tp)))                    
            # Condition to send request
            send_request =  (current_price >= tp_level) if order_type == 1 else (current_price <= tp_level)                        
            if send_request:                                        
                request_structure["sl"] = new_sl
                request_structure["tp"] = tp                      
                open_price = new_sl                
        else:
            lowest,highest = Technical(data_m1).get_lowest_and_highest() 
            difference = abs(highest - lowest)
            fibonacci_levels = {
                11.2: .112* difference,
                23.6: .236 * difference,
                38.2: .382 * difference,        
                50: .5 * difference,
                61.8: .618 * difference
            }                          
            operation = operator.add if order_type == 1 else operator.sub        
            tp1 = format_values(operation(open_price,fibonacci_levels[23.6]))
            tp2 = format_values(operation(open_price,fibonacci_levels[50]))  
            sl1 = format_values(operation(open_price,fibonacci_levels[11.2])) 
            sl2 = format_values(operation(open_price,fibonacci_levels[38.2]))             
            # Set SL1
            if tp1 <= current_price < tp2:                                   
                request_structure["sl"] = sl1
                request_structure["tp"] = tp    
                send_request = True
            # Set SL2
            elif tp2 <= current_price:
                request_structure["sl"] = sl2
                request_structure["tp"] = tp    
                send_request = True                                    
        # Check PnL if kwargs were passed otherwise skip
        if "profit" or "loss" in kwargs:            
            current_pnl = mt5_connection.account_details().profit
            # Close trades if a condition is met
            if current_pnl <= kwargs["loss"] or current_pnl >= kwargs["profit"]:                
                close_trades(mt5_connection)
                break    
        # Check flag_session if was passed otherwise skip
        if "flag_session" in kwargs:
            if kwargs["flag_session"]:
                close_trades(mt5_connection)
                break
        # Send request to the MT5 server if any trailling_type returns true
        if send_request:
            for i in range(len(trades_dict)):
                request_structure["ticket"] = trades_dict[i]["ticket"]
                result = mt5.order_send(request_structure)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    print(f'Trade updated')              
            # Close one trade 
            if partial_close and len(trades_dict) > 1:
                ticket_to_close,order_to_close,volume = trades_dict[0]["ticket"], trades_dict[0]["type"],trades_dict[0]["volume"]    
                mt5_connection.close_position(symbol, ticket_to_close, order_to_close, volume,"Partial Close")
            send_request = False         
        # Update main variables to control the loop
        try: 
            trades = mt5_connection.get_positions(0,symbol)[["symbol", "ticket", "type", "volume","sl","tp"]]   
            trades_dict = trades.T.to_dict()                                                                 
        except Exception as e:
            print("Exception raised: ",e)
        sleep(1)
                