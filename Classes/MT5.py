import pandas as pd
import numpy as np
import pytz
import mplfinance as mpl
import datetime as dt
import sys
import MetaTrader5 as mt5
            
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

class MT5:
    
    # Define Global attributes
    time_frames = {
        "M1": mt5.TIMEFRAME_M1,
        "M2": mt5.TIMEFRAME_M2,
        "M3": mt5.TIMEFRAME_M3,
        "M4": mt5.TIMEFRAME_M4,
        "M5": mt5.TIMEFRAME_M5,
        "M6": mt5.TIMEFRAME_M6,
        "M10": mt5.TIMEFRAME_M10,
        "M12": mt5.TIMEFRAME_M12,
        "M15": mt5.TIMEFRAME_M15,
        "M20": mt5.TIMEFRAME_M20,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H2": mt5.TIMEFRAME_H2,
        "H3": mt5.TIMEFRAME_H3,
        "H4": mt5.TIMEFRAME_H4,
        "H6": mt5.TIMEFRAME_H6,
        "H8": mt5.TIMEFRAME_H8,
        "H12": mt5.TIMEFRAME_H12,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1
    }
    utc_from = None
    utc_to = None
    date = None    
    timezone = pytz.timezone("Etc/UTC")
    #timezone = pytz.timezone('America/Mexico_City')
    # Tuple with all the symbols
    group_symbols = mt5.symbols_get()

    # Constructor method every time we want to create a new object
    def __init__(self, user, password, server):
        self.user = user
        self.password = password
        self.server = server
        self.connection_state = False
        self.start()        

    def start(self):
        user = self.user
        password = self.password
        server = self.server       
        # Establish MetaTrader 5 connection to a specified trading account
        if not mt5.initialize(login=user, server=server, password=password):            
            self.error = mt5.last_error()
            print("initialize() failed, error code =", self.error)            
            sys.exit()            
        print("Successfully Connection! \n")
        self.connection_state = True        
        

    # Get object with all details
    def account_details(self, show=0):
        # authorized = mt5.login(self.user, password=self.password, server=self.server)
        # if authorized:
        try:
            account_info = mt5.account_info()            
        except:
            print("failed to connect at account #{}, error code: {}".format(self.user, mt5.last_error()))

        if show != 0:
            print(account_info)

        # Account object
        return account_info

    # Display all available symbols with the spread passed
    def display_symbols(self, elements, sprd=3):
        """ 
            Display the symbols with a spread less than te input user, this function also return a list with the rest
            of attributes from the symbols
        """

        lenght = len(elements)

        # Define the first elem in the list
        string = f'*{elements[0]}*'
        new_list = list()

        # Create a list to concatenate the elems and get the format to pass as parameter
        if not len(elements) == 1:
            for i in range(1, lenght):
                new_list.append(f'*{elements[i]}*')

        final_string = string
        for elem in new_list:
            final_string += "," + elem


        self.group_symbols = mt5.symbols_get(group=final_string)
        group_return = list()

        for e in self.group_symbols:
            if not e.spread > sprd:
                group_return.append(e)

        return group_return

    # Display orders opened
    def get_deals(self, ticket=0, show=1):
        if ticket == 0:
            return pd.DataFrame()
        else:
            try:
                deals = mt5.history_deals_get(position=int(ticket))
                df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
                df['time'] = pd.to_datetime(df['time'], unit='s')
                if show == 1:
                    print(df)
                return df
            except:
                print("Error in get deals!")
        return pd.DataFrame()    
        
        
    def get_positions(self, show=1,s=None,id=None):
        """
            Get the positions opened to extract the info and close it with the function below
        """
        if s is not None and id is None:
            info_position = mt5.positions_get(symbol=s)
        elif id is not None and s is None:
            info_position = mt5.positions_get(ticket=id)
        else:
            info_position = mt5.positions_get()                    

        if info_position is None or len(info_position) == 0:
            if show == 1:
                print("No positions were found!")
                df = pd.DataFrame()
            else:
                df = pd.DataFrame()

        elif len(info_position) > 0:
            df = pd.DataFrame(list(info_position), columns=info_position[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    # Send request to open a position
    def open_position(self,symbol,operation,lot,points=40,comment="Python"):
        """
            This method send the request to open a position with the paramateres
        """        
        # prepare the request structure        
        symbol_info = mt5.symbol_info(symbol)
        
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")                        
        
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)                                
                
        point = mt5.symbol_info(symbol).point        
        deviation = 20
                        
        price = mt5.symbol_info_tick(symbol).ask if operation == 1 else  mt5.symbol_info_tick(symbol).bid
        decimal_places = len(str(price).split(".")[1])        
        # Open position based on points
        if type(points) is int:            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,     
                "type": mt5.ORDER_TYPE_BUY if operation == 1 else  mt5.ORDER_TYPE_SELL,
                "price": price,
                "tp": price + (points * point) if operation == 1 else price - (points * point),
                "sl": round(price - ((points / 2) * point),decimal_places) if operation == 1 else round(price + ((points / 2) * point),decimal_places),
                "deviation": deviation,
                #"magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                }        
        # Set SL and TP passed
        else:
             request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,     
                "type": mt5.ORDER_TYPE_BUY if operation == 1 else  mt5.ORDER_TYPE_SELL,
                "price": price,
                "tp": points[1],
                "sl": points[0],
                "deviation": deviation,
                #"magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
                }  
            
        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))        
        if result is None:
            print("2. order_send failed, no response received")
            return 0
        elif result.retcode != mt5.TRADE_RETCODE_DONE:                                                   
            print("2. order_send failed, retcode={}".format(result.retcode))
            if result.retcode == 10031:
                print("Trade Server connection lost")  
            elif result.retcode == 10019:
                print("Lack of free margin to execute the Order")                                 
                return 10019
            # request the result as a dictionary and display it element by element
            #result_dict=result._asdict()    
            return 0                                                                           
        return np.int64(result.order)
    # Send request to close position
    def close_position(self, stock, ticket, type_order, vol, comment="Close",display=False):
        if (type_order == 1):
            request_close = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": stock,
                "volume": vol,
                "type": mt5.ORDER_TYPE_SELL,
                "position": int(ticket),
                "price": mt5.symbol_info_tick(stock).bid,
                "deviation": 20,
                # "magic": 0,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,  # mt5.ORDER_FILLING_RETURN,
            }
            result = mt5.order_send(request_close)
            print(result)

        else:
            request_close = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": stock,
                "volume": vol,
                "type": mt5.ORDER_TYPE_BUY,
                "position": int(ticket),
                "price": mt5.symbol_info_tick(stock).ask,
                "deviation": 20,
                # "magic": 0,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,  # mt5.ORDER_FILLING_RETURN,
            }
            result = mt5.order_send(request_close)
            if display:
                print(result)

    # Get data for the selected symbols and timeframe
    def data_range(self, symbol, temp, times, plot=0):
        self.utc_to = dt.datetime.now(tz=self.timezone) + dt.timedelta(hours=8)
        self.utc_from = self.utc_to - dt.timedelta(minutes=times)
        self.bars = times
        self.rates = mt5.copy_rates_from(symbol, self.time_frames[temp], self.utc_from, self.bars)
        # Create a DataFrame from the obtained data
        rates_frame = pd.DataFrame(self.rates)
        # Convert time in seconds into the datetime format
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame["time"] = rates_frame["time"] - pd.Timedelta(hours=9)
        rates_frame = rates_frame.set_index('time')        
        # Plot the graph
        if not plot == 0:
            mpl.plot(rates_frame, type="candle", style="classic", title=str(symbol + " " + temp))
        return rates_frame
    def calculate_profit(self,symbol,points,lot,order):                
        point=mt5.symbol_info(symbol).point
        symbol_tick=mt5.symbol_info_tick(symbol)
        ask=symbol_tick.ask
        bid=symbol_tick.bid        
        if order == 1:
            profit=mt5.order_calc_profit(mt5.ORDER_TYPE_BUY,symbol,lot,ask,ask+points*point)                    
        else:
            profit=mt5.order_calc_profit(mt5.ORDER_TYPE_SELL,symbol,lot,bid,bid-points*point)
        return profit
    # Close the connection with MT5
    def close(self):
        mt5.shutdown()
        print("Closed Connection!")        
    
    
