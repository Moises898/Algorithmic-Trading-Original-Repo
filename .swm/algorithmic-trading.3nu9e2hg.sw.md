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

<SwmSnippet path="Classes/MT5.py" line="43">

---

### **Constructor Method**

### Parameters

1. User --> int

2. Password --> str

3. Server --> str

Create an object to enable the connection with MT5

```
    def __init__(self, user, password, server):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="53" collapsed>

---

### **start()**

Stablish a connection to the Metatrader 5 server.

```
    def start(self):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="70">

---

### **account_details(show=0)**

Return an object of type AccountInfo from Metatrader 5 library.\
*Note: Method don't display info by default pass 1 as arg to print to the console.*

```
    def account_details(self, show=0):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="86">

---

### **display_symbols(elements,spread=10)**

### **Parameters**

1. elements --> list

2. spread --> int

Display symbols that follows the criteria passed (spread, keyword symbol).

This method by default filter spread less than 10 and return a list with the symbols information.

```
    def display_symbols(self, elements, spread=10):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="121">

---

### get_deals(ticket=0,show=1)

### **Parameters**

1. ticket --> int

2. show --> int

Display orders from the MT5 server.

```
    def get_deals(self, ticket=0, show=1):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="143">

---

### get_positions(show=1,symbol=None,id=None)

### **Parameters**

1. show --> int

2. symbol --> str

3. id --> int

Get orders woth their correspondent info to close or monitor.

```
    def get_positions(self, show=1, symbol=None, id=None):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="170">

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

```
    def open_position(self, symbol, operation, lot, points=40, comment="Python"):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="250">

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

```
    def close_position(self, symbol, ticket, type_order, vol, comment="Close", display=False):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="297">

---

### **get_data(symbol, temp, n_periods, plot=0)**

### Parameters

1. <SwmToken path="/Classes/MT5.py" pos="297:8:8" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`symbol`</SwmToken>: Name of the symbol --> str

2. <SwmToken path="/Classes/MT5.py" pos="297:11:11" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`temp`</SwmToken>: TimeFrame to get data (M1,M3,H1) --> str

3. <SwmToken path="/Classes/MT5.py" pos="297:14:14" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`n_periods`</SwmToken>: Number of candles to get from current time (Current time - n_periods) --> int

4. <SwmToken path="/Classes/MT5.py" pos="297:17:17" line-data="    def get_data(self, symbol, temp, n_periods, plot=0):">`plot`</SwmToken>: Display a chart in japanese format (1 - Display) --> int

Retrive data from the passed symbol from current time less the number of periods passed.

```
    def get_data(self, symbol, temp, n_periods, plot=0):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="323">

---

### **calculate_profit(symbol,points,lot,order)**

### Parameters

1. <SwmToken path="/Classes/MT5.py" pos="323:8:8" line-data="    def calculate_profit(self, symbol, points, lot, order):">`symbol`</SwmToken>:Name of the symbol --> str

2. <SwmToken path="/Classes/MT5.py" pos="323:11:11" line-data="    def calculate_profit(self, symbol, points, lot, order):">`points`</SwmToken>: Number of points to calculate the profit/loss --> int

3. <SwmToken path="/Classes/MT5.py" pos="327:21:21" line-data="        @param symbol: Name of the symbol to estimate profit/lots.">`lots`</SwmToken>: Size of the simulated trade --> float/int

4. <SwmToken path="/Classes/MT5.py" pos="323:17:17" line-data="    def calculate_profit(self, symbol, points, lot, order):">`order`</SwmToken>: BUY (1) or SELL (0) --> int

This method allow you to calculate the profit or loss without need to open trades.

```
    def calculate_profit(self, symbol, points, lot, order):
```

---

</SwmSnippet>

<SwmSnippet path="Classes/MT5.py" line="344">

---

### **close()**

Close the connection to the MT6 server.

```
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

### **Constructor method**

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

### <SwmToken path="/Classes/technical.py" pos="40:3:4" line-data="    def get_bar_direction(self, lenght):">`get_bar_direction(`</SwmToken> <SwmToken path="/Classes/technical.py" pos="40:8:8" line-data="    def get_bar_direction(self, lenght):">`lenght`</SwmToken>**)**

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

<SwmSnippet path="/Classes/technical.py" line="64">

---

### **EMA(** <SwmToken path="/Classes/technical.py" pos="65:8:12" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=-1):">`entry="close"`</SwmToken>**,** <SwmToken path="/Classes/technical.py" pos="65:15:17" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=-1):">`period=12`</SwmToken>**,** <SwmToken path="/Classes/technical.py" pos="65:19:21" line-data="    def EMA(self, entry=&quot;close&quot;, period=12,deviation=-1):">`deviation=-1`</SwmToken>**)**

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
