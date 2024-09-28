---
title: |
  Algorithmic Trading
---
# ATLAS

## **Introduction**

This module use the Metatatrader5 library to connect with the platform, the functions were adapted to launch operations with own parameters and [conditions.To](http://conditions.To) know more information about the functions of Metatrade5, please refer the next documentation:\
<https://www.mql5.com/en/docs/integration/python_metatrader5>

Next you can read more about each function and how to implement it.

# **MT5 Class**

This class is a wrapper for the MT5 library that contains all related methods to interact with Metatrader 5 such as:

- Stablish Connection
- Retrieve data
- Open Trades
- Close Trades
- Get Account Info

<SwmSnippet path="/Classes/MT5.py" line="43" collapsed>

---

### **Constructor Method**

### Parameters

1. User --> int

2. Password --> str

3. Server --> str

Create an object to enable the connection with MT5

```python
    def __init__(self, user, password, server):
        self.error = None
        self.rates = None
        self.bars = None
        self.user = user
        self.password = password
        self.server = server
        self.connection_state = False
        self.start()
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="53" collapsed>

---

### **start()**

Stablish a connection to the Metatrader5 server.

```python
    def start(self):
        """
            Start connection to the MT5 server.
        """
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
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="70" collapsed>

---

### **account_details(show=0)**

Return an object of type AccountInfo from Metatrader5 library.\
*Note: Method don't display info by default pass 1 as arg to print to the console.*

```python
    def account_details(self, show=0):
        # authorized = mt5.login(self.user, password=self.password, server=self.server)
        # if authorized:
        account_info = None
        try:
            account_info = mt5.account_info()
        except:
            print("failed to connect at account #{}, error code: {}".format(self.user, mt5.last_error()))

        if show != 0:
            print(account_info)

        # Account object
        return account_info
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="85" collapsed>

---

### **display_symbols(elements,spread=10)**

### **Parameters**

1. elements --> list

2. spread --> int

Display symbols that follows the criteria passed (spread, keyword symbol).

This method by default filter spread less than 10 and return a list with the symbols information.

```python
    # Display all available symbols with the spread passed
    def display_symbols(self, elements, spread=10):
        """ 
            Display the symbols with a spread less than te input user, this function also return a list with the rest
            of attributes from the symbols.

            @param spread: Max value of spread to display symbols
            @param elements: Str to retrieve symbols e.g (EUR,USD,XAUUSD)
            @return: pandas DataFrame --> Orders info
        """

        lenght = len(elements)

        # Define the first elem in the list
        string = f'*{elements[0]}*'
        new_list = list()

        # Create a list to concatenate the elements and get the format to pass as parameter
        if not len(elements) == 1:
            for i in range(1, lenght):
                new_list.append(f'*{elements[i]}*')

        final_string = string
        for elem in new_list:
            final_string += "," + elem

        self.group_symbols = mt5.symbols_get(group=final_string)
        group_return = list()

        for e in self.group_symbols:
            if not e.spread > spread:
                group_return.append(e)

        return group_return
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="120" collapsed>

---

### get_deals(ticket=0,show=1)

### **Parameters**

1. ticket --> int

2. show --> int

Display orders from the MT5 server.

```python
    # Display orders opened
    def get_deals(self, ticket=0, show=1):
        """
            Display orders from the MT5 history server

            @param ticket: Order ID from the trade
            @param show: Display DataFrame in the console
            @return: pandas DataFrame --> Orders info
        """
        if ticket == 0:
            return pd.DataFrame()
        else:
            try:
                deals = mt5.history_deals_get(position=int(ticket))
                df: DataFrame = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
                df['time'] = pd.to_datetime(df['time'], unit='s')
                if show == 1:
                    print(df)
                return df
            except:
                print("Error in get deals!")
        return pd.DataFrame()
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="143" collapsed>

---

### get_positions(show=1,symbol=None,id=None)

### **Parameters**

1. show --> int

2. symbol --> str

3. id --> int

Get orders woth their correspondent info to close or monitor.

```python
    def get_positions(self, show=1, symbol=None, id=None):
        """
            Get the positions opened to extract the info and close it with the function below

            @param show: Display message in console
            @param symbol: Symbol name to check for open trades
            @param id: ID to check for open trades
            @return: pandas DataFrame
        """
        df = pd.DataFrame()
        if symbol is not None and id is None:
            info_position = mt5.positions_get(symbol=symbol)
        elif id is not None and symbol is None:
            info_position = mt5.positions_get(ticket=id)
        else:
            info_position = mt5.positions_get()

        if info_position is None or len(info_position) == 0:
            if show == 1:
                print("No positions were found!")

        elif len(info_position) > 0:
            df = pd.DataFrame(list(info_position), columns=info_position[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="169" collapsed>

---

### **open_position(symbol,operation,lot,points=40,comment="Python")**

### **Parameters**

1. symbol: Name of the symbol exactly as in the broker appears --> str

2. operation: BUY(1), SELL(0) --> int

3. lot: Size of the operation to open --> int

4. points: --> list/str

   - a) Number of points to set the SL and TP from the entry poitnt, points are calculated automatically based on the symbol.

   - b) \[SL,TP\] a list with an specific price where the SL and TP should be set.

5. comment: Comment displayed in the MT5 console.

Send request to the server to open a trade with passed args.

```python
    # Send request to open a position
    def open_position(self, symbol, operation, lot, points=40, comment="Python"):
        """
            Send the request to the MT5 server to open a trade with args passed.

            @param symbol: Symbol to open the trade
            @param operation: BUY (1) / SELL (0)
            @param lot: Size Operation (int)
            @param points: Points to set up SL/TP or list with SL/TP values
            @param comment: Comment appears into the MT5 console
            @return: Order ID (int)
        """
        # prepare the request structure
        symbol_info = mt5.symbol_info(symbol)

        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")

            # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)

        point = mt5.symbol_info(symbol).point
        deviation = 20

        price = mt5.symbol_info_tick(symbol).ask if operation == 1 else mt5.symbol_info_tick(symbol).bid
        decimal_places = len(str(price).split(".")[1])
        # Open position based on points
        if type(points) is int:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY if operation == 1 else mt5.ORDER_TYPE_SELL,
                "price": price,
                "tp": price + (points * point) if operation == 1 else price - (points * point),
                "sl": round(price - ((points / 2) * point), decimal_places) if operation == 1 else round(
                    price + ((points / 2) * point), decimal_places),
                "deviation": deviation,
                # "magic": 234000,
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
                "type": mt5.ORDER_TYPE_BUY if operation == 1 else mt5.ORDER_TYPE_SELL,
                "price": price,
                "tp": points[1],
                "sl": points[0],
                "deviation": deviation,
                # "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

        # Send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
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
            return 0
        return np.int64(result.order)
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="250" collapsed>

---

### **close_position(symbol,ticket,type_order)**

### Parameters

1. <SwmToken path="/Classes/MT5.py" pos="250:8:8" line-data="    def close_position(self, symbol, ticket, type_order, vol, comment=&quot;Close&quot;, display=False):">`symbol`</SwmToken>: Name of the symbol to close the trade --> str

2. <SwmToken path="/Classes/MT5.py" pos="250:11:11" line-data="    def close_position(self, symbol, ticket, type_order, vol, comment=&quot;Close&quot;, display=False):">`ticket`</SwmToken>: ID of the trade --> str

3. <SwmToken path="/Classes/MT5.py" pos="250:14:14" line-data="    def close_position(self, symbol, ticket, type_order, vol, comment=&quot;Close&quot;, display=False):">`type_order`</SwmToken>: BUY (1) or SELL (0) --> int

4. <SwmToken path="/Classes/MT5.py" pos="250:17:17" line-data="    def close_position(self, symbol, ticket, type_order, vol, comment=&quot;Close&quot;, display=False):">`vol`</SwmToken>: Size of the trade --> float

5. <SwmToken path="/Classes/MT5.py" pos="250:20:20" line-data="    def close_position(self, symbol, ticket, type_order, vol, comment=&quot;Close&quot;, display=False):">`comment`</SwmToken>: Comment to sent (Close by default) --> str

This method create and send the request to close the position with passed args.

To get the required args we can use the get_positions() method and select one of the current open positions from the DataFrame or manually pass.

```python
    def close_position(self, symbol, ticket, type_order, vol, comment="Close", display=False):
        """
            Close Open trade from MT5 Server

            @param symbol: Name of the Symbol
            @param ticket: ID of the trade
            @param type_order: BUY (1) or SELL (0)
            @param vol: Size of the trade
            @param comment: Comment to add to the order
            @param display: Display in console
        """
        if type_order == 1:
            request_close = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": vol,
                "type": mt5.ORDER_TYPE_SELL,
                "position": int(ticket),
                "price": mt5.symbol_info_tick(symbol).bid,
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
                "symbol": symbol,
                "volume": vol,
                "type": mt5.ORDER_TYPE_BUY,
                "position": int(ticket),
                "price": mt5.symbol_info_tick(symbol).ask,
                "deviation": 20,
                # "magic": 0,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,  # mt5.ORDER_FILLING_RETURN,
            }
            result = mt5.order_send(request_close)
            if display:
                print(result)
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="296" collapsed>

---

### **get_data(symbol, temp, n_periods, plot=0)**

### Parameters

1. <SwmToken path="/Classes/MT5.py" pos="297:8:8" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`symbol`</SwmToken>: Name of the symbol --> str

2. <SwmToken path="/Classes/MT5.py" pos="297:11:11" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`temp`</SwmToken>: TimeFrame to get data (M1,M3,H1) --> str

3. <SwmToken path="/Classes/MT5.py" pos="297:14:14" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`n_periods`</SwmToken>: Number of candles to get from current time (Current time - n_periods) --> int

4. <SwmToken path="/Classes/MT5.py" pos="297:17:17" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`plot`</SwmToken>: Display a chart in japanese format (1 - Display) --> int

```python
    # Get data for the selected symbols and timeframe
    def get_data(self, symbol, temp, n_periods, plot=0):
        """
            Retrieve data from the symbol passed from current time less the number of periods passed

        @param symbol: Name of the symbol to get data
        @param temp: TimeFrame to retrieve data.
        @param n_periods: Number of periods to retrieve from current time.
        @param plot: Display a chart in japanese format
        @return: pandas DataFrame --> candles information
        """

        self.utc_to = dt.datetime.now(tz=self.timezone) + dt.timedelta(hours=8)
        self.utc_from = self.utc_to - dt.timedelta(minutes=n_periods)
        self.bars = n_periods
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
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="323" collapsed>

---

### **calculate_profit(symbol,points,lot,order)**

### Parameters

1. <SwmToken path="/Classes/MT5.py" pos="323:8:8" line-data="    def calculate_profit(self, symbol, points, lot, order):">`symbol`</SwmToken>:Name of the symbol --> str

2. <SwmToken path="/Classes/MT5.py" pos="323:11:11" line-data="    def calculate_profit(self, symbol, points, lot, order):">`points`</SwmToken>: Number of points to calculate the profit/loss --> int

3. <SwmToken path="/Classes/MT5.py" pos="327:21:21" line-data="        @param symbol: Name of the symbol to estimate profit/lots.">`lots`</SwmToken>: Size of the simulated trade --> float/int

4. <SwmToken path="/Classes/MT5.py" pos="323:17:17" line-data="    def calculate_profit(self, symbol, points, lot, order):">`order`</SwmToken>: BUY (1) or SELL (0) --> int

This method allow you to calculate the profit or loss without need to open trades.

```python
    def calculate_profit(self, symbol, points, lot, order):
        """
            Calculate estimated profit or loss by symbol, lot size, order and points.

        @param symbol: Name of the symbol to estimate profit/lots.
        @param points: Number of points.
        @param lot: Size  operation
        @param order: BUY(1) or SELL (0)
        @return: int --> estimated profit/loss

        """
        point = mt5.symbol_info(symbol).point
        symbol_tick = mt5.symbol_info_tick(symbol)
        ask = symbol_tick.ask
        bid = symbol_tick.bid
        if order == 1:
            profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, lot, ask, ask + points * point)
        else:
            profit = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL, symbol, lot, bid, bid - points * point)
        return profit
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/MT5.py" line="344" collapsed>

---

### **close()**

Close the connection to the MT6 server.

```python
    # Close the connection with MT5
    def close(self):
        """
            Close connection to the server
        """
        mt5.shutdown()
        print("Closed Connection!")
```

---

</SwmSnippet>

# Technical Class

*Contains multiple types of technical analysis, it is based in TA-Lib and modified for personal use with extra features. To know more information about the functions of TA-Lib, please refer the next documentation: [https://mrjbq7.github.io/ta-lib/index.html](https://mrjbq7.github.io/ta-lib/index.html)*

&nbsp;

<SwmSnippet path="/Classes/technical.py" line="26" collapsed>

---

### ***Constructor method***

*To start applying technical analysis a pandas DataFrame needs to be passed you can retrive this from the* <SwmToken path="/Classes/MT5.py" pos="297:3:3" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`get_data`</SwmToken> *method from the  or pass any pandas DataFrame that follows the same format as* <SwmToken path="/Classes/MT5.py" pos="297:3:3" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`get_data`</SwmToken> *method.*

### Parameters

1. df --> pandas DataFrame

Create an object to start calling the methos and perform techncial analysis.

*Note: The contructor method call internal methods to set default attributes such as bar trends.*

```python
    def __init__(self, df=None):
        """
        Create a Technical object to acces all the technical analysis fucntions.

        Args:
            df (pandas dataframe, optional): DataFrame object to calculate values. Defaults to None.
        """
        self.df = df
        self.get_previous_bar_trend()
        self.get_current_bar_trend()
        self.df = self.df.copy()
        self.df["hl2"] = (self.df["high"]+self.df["low"])/2
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/technical.py" line="39" collapsed>

---

### ***get_bar_direction(*** <SwmToken path="/Classes/technical.py" pos="40:8:8" line-data="    def get_bar_direction(self, lenght):">`lenght`</SwmToken>***)***

### Parameters

1. lenght--> int

Retrieve a list with the trend of each bar such as:

- Uptrend (1)
- Dowtrend (-1)
- Neutral (2)

```python
    # Return the direction of each bar
    def get_bar_direction(self, lenght):
        """
        Determine the direction of each bar from the dataFrame based on the open and close price.

        Args:
            lenght (int): Number of periods to get directions from the DataFrame

        Returns:
            list: A list of up or down trend for each bar.
        """
        df = self.df
        directions = []
        for bar in df[-lenght:].index:
            if df.loc[bar]["open"] < df.loc[bar]["close"]:
                # Bullish bar
                directions.append(1)
            elif df.loc[bar]["open"] > df.loc[bar]["close"]:
                # Bearish bar
                directions.append(-1)
            else:
                # Doji bar
                directions.append(2)
        return directions
```

---

</SwmSnippet>

<SwmSnippet path="/Classes/technical.py" line="64" collapsed>

---

### ***EMA(*** <SwmToken path="/Classes/technical.py" pos="65:8:12" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=-1):">`entry="close"`</SwmToken>***,*** <SwmToken path="/Classes/technical.py" pos="65:15:17" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=-1):">`period=12`</SwmToken>***,*** <SwmToken path="/Classes/technical.py" pos="65:19:21" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=1):">`deviation=1`</SwmToken>***)***

### Parameters

1. entry: Column used to calculate the EMA values --> str

2. period: Number of periods used to calculate the EMA values --> int

3. deviation: Offset used to retrieve the EMA values --> int

Retrieve a list with the trend of each bar such as:

- Uptrend (1)
- Dowtrend (-1)
- Neutral (2)

```python
    # Exponential Moving Averge indicator
    def EMA(self, entry="close", period=12,deviation=-1):
        """
        Calculate an Exponential Moving Average based on the args passed.

        Args:
            entry (str, optional): Column to use to calculate the EMA . Defaults is to "close".
            period (int, optional): Number of periods to calculate the EMA . Defaults is to 12.
            deviation (int, optional): Offset the last values to get a deviation of n_periods. Defaults to -1.

        Returns:
            list : List of the the values for each time of period of the dataFrame.
        """
        df = self.df
        ema = ta.EMA(df[entry], timeperiod=period)
        if deviation > 0:            
            ema = ema[:-deviation]
        return ema
```

---

</SwmSnippet>

&nbsp;

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBQWxnb3JpdGhtaWMtVHJhZGluZyUzQSUzQU1vaXNlczg5OA==" repo-name="Algorithmic-Trading"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
