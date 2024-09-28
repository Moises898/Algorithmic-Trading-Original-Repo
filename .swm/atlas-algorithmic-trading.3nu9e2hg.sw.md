---
title: |
  ATLAS Algorithmic Trading
---
## **Introduction**

This module use the Metatatrader5 library to connect with the platform, the functions were adapted to launch operations with own parameters and conditions.To know more information about the functions of Metatrade5, please refer the next documentation:\
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

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBQWxnb3JpdGhtaWMtVHJhZGluZyUzQSUzQU1vaXNlczg5OA==" repo-name="Algorithmic-Trading"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
