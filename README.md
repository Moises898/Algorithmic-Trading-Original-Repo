# ATLAS Algorithmic Trading

- [ATLAS Algorithmic Trading](#atlas-algorithmic-trading)
- [MT5 Class](#mt5-class)
  - [Constructor Method](#constructor-method)
    - [Parameters](#parameters)
    - [Example:](#example)
  - [start()](#start)
    - [Example:](#example-1)
  - [close()](#close)
    - [Example:](#example-2)
  - [account\_details(show=0)](#account_detailsshow0)
    - [Example:](#example-3)
  - [display\_symbols(elements,spread=10)](#display_symbolselementsspread10)
    - [Parameters](#parameters-1)
    - [Example:](#example-4)
  - [open\_position(symbol,operation,lot,points=40,comment="Python")](#open_positionsymboloperationlotpoints40commentpython)
    - [Parameters](#parameters-2)
    - [Example:](#example-5)
  - [get\_positions(show,symbol,id)](#get_positionsshowsymbolid)
    - [Parameters](#parameters-3)
    - [Example:](#example-6)
  - [close\_position(symbol,ticket,type\_order)](#close_positionsymboltickettype_order)
    - [Parameters](#parameters-4)
    - [Examples:](#examples)
  - [get\_data(symbol, temp, n\_periods, plot=0)](#get_datasymbol-temp-n_periods-plot0)
    - [Parameters](#parameters-5)
    - [Example:](#example-7)
  - [calculate\_profit(symbol,points,lot,order)](#calculate_profitsymbolpointslotorder)
    - [Parameters](#parameters-6)
    - [Examples](#examples-1)
- [Technical Class](#technical-class)
  - [Constructor method](#constructor-method-1)
    - [Example:](#example-8)
  - [get\_bars\_direction(lenght)](#get_bars_directionlenght)
    - [Parameters](#parameters-7)
    - [Example:](#example-9)
  - [EMA(entry = "close", period = 12, deviation=-1)](#emaentry--close-period--12-deviation-1)
    - [Parameters](#parameters-8)
    - [Example:](#example-10)
  - [SMA(entry = "close", period = 12, deviation=-1)](#smaentry--close-period--12-deviation-1)
    - [Parameters](#parameters-9)
    - [Example:](#example-11)
  - [calculate\_middle\_price(period=10)](#calculate_middle_priceperiod10)
    - [Parameters](#parameters-10)
    - [Example:](#example-12)
  - [calculate\_roc(entry="open", period=8)](#calculate_rocentryopen-period8)
    - [Parameters](#parameters-11)
    - [Example:](#example-13)
  - [calculate\_avg\_price()](#calculate_avg_price)
    - [Example:](#example-14)
  - [get\_previous\_bar\_trend()](#get_previous_bar_trend)
    - [Example](#example-15)
  - [get\_current\_bar\_trend()](#get_current_bar_trend)
    - [Example](#example-16)
  - [calculate\_trend\_by\_bars\_trend(n\_periods=0)](#calculate_trend_by_bars_trendn_periods0)
    - [Parameters](#parameters-12)
    - [Example](#example-17)
  - [calculate\_trend\_by\_trendline(n\_periods=0)](#calculate_trend_by_trendlinen_periods0)
    - [Parameters](#parameters-13)
    - [Example](#example-18)
  - [calculate\_chopiness\_index(lookback=6)](#calculate_chopiness_indexlookback6)
    - [Parameters](#parameters-14)
    - [Example](#example-19)
  - [calculate\_trend\_angle(n\_periods=50)](#calculate_trend_anglen_periods50)
    - [Parameters](#parameters-15)
    - [Example:](#example-20)
  - [get\_lowest\_and\_highest(lenght=10)](#get_lowest_and_highestlenght10)
    - [Parameters](#parameters-16)
    - [Example:](#example-21)
  - [calculate\_super\_trend(atr\_period=15, multiplier=3)](#calculate_super_trendatr_period15-multiplier3)
    - [Parameters](#parameters-17)
    - [Example:](#example-22)

<h2>Introduction</h2>
<p>This module use the Metatatrader5 library to connect with the platform, the functions were adapted to launch operations with own parameters and conditions.To know more information about the functions of Metatrade5, please refer the next documentation:<br> 
https://www.mql5.com/en/docs/integration/python_metatrader5 </p>

<p>Next you can read more about each function and how to implement it.</p>



# MT5 Class

This class is a wrapper for the MT5 library that contains all related methods to interact with Metatrader 5 such as: 

<li>Stablish Connection</li>
<li>Retrieve data</li>
<li>Open Trades</li>
<li>Close Trades</li>
<li>Get Account Info</li>

## Constructor Method

<p>Create an object to enable the connection with MT5

### Parameters
<ol>
<li>User --> int</li>
<li>Password --> str</li>
<li>Server --> str</li>
</ol>

### Example:
    
    user = 12345
    password = "passwd123"
    server = "MetaQuotes-Demo"
    conn = MT5(user,password,server)

<i>Note: By default the contructor method call the start method to start the connection to the MT5 server</i>
</p>


## start()
<p>Stablish a connection to the Metatrader5 server.<br>

### Example:
    
    conn.start()
</p>


## close()
<p>Close the connection to Metatrader5 server.<br>

### Example:
        
    conn.close()
</p>



## account_details(show=0)
<p>Return an object of type AccountInfo from Metatrader5 library. <br>
<i>Note: Method don't display info by default pass 1 as arg to print to the console.</i><br>

### Example:

    #Display object with attributes
    conn.account_details()
<br>

    # Save balance attribute
    balance = conn.account_details().balance

</p>

## display_symbols(elements,spread=10)

### Parameters
<ol>
    <li>elements --> list</li>
    <li>spread --> int</li>
</ol>

<p>Display symbols that follows the criteria passed (spread, keyword symbol). <br>

This method by default filter spread less than 10 and return a list with the symbols information.<br>

### Example:
    
    #Filter the symbols that contains "EUR" and spread less than 5 
    symbols = conn.display_symbols(["EUR"],5)    
</p>


## open_position(symbol,operation,lot,points=40,comment="Python")

### Parameters

<ol>
    <li>symbol: Name of the symbol exactly as in the broker appears --> str</li>
    <li>operation: BUY(1), SELL(0) --> int</li>
    <li>lot: Size of the operation to open --> int </li>
    <li>points: --> list/str</li>
        <ul>a) Number of points to set the SL and TP from the entry poitnt, points are calculated automatically based on the symbol.</ul>
        <ul>b) [SL,TP] a list with the specific price where the SL and TP should be set.</ul>
    <li>comment: Comment displayed in the MT5 console.</li>
</ol>
<br>

<p>This method create and send a request to execute the position with the input parameters.<br>

<i><b>Note: Use the display_symbols() to retrive the name and pass it correctly.</b></i></p>


### Example: 

<b>SELL 0.2 lots in EURUSD with 40 points as SL/TP</b>

    order_id = conn.open_position("EURUSD",0,0.2,40,"This trade was executed from my code")    
</p>

## get_positions(show,symbol,id)

### Parameters

<ol>
    <li>show: Display message in the console --> int</li>
    <li>symbol: Get trades info with symbol passed --> str</li>
    <li>id: Get trade info with the ID passed --> str</li>
</ol>

<p>Returns a pandas dataframe with trades open if exists.
<br>

### Example: 

    df = conn.get_positions()   
</p>

## close_position(symbol,ticket,type_order)

### Parameters

<ol>
    <li>symbol:Name of the symbol to close the trade --> str</li>
    <li>ticket: ID of the trade --> str </li>
    <li>type_order: BUY (1) or SELL (0) --> int </li>
    <li>vol: Size of the trade --> float </li>
    <li>comment: Comment to sent (Close by default) --> str</li>
</ol>

<p>This method create and send the request to close the position with passed args.<br>

To get the required args we can use the [get_positions](#get_positionsshowsymbolid) method and select one of the current open positions from the dataFrame or manually pass.
<br>

### Examples:
<b>Assigning the values from the columns to variables</b>
   
    df = conn.get_positions()
    type_ord = df["type"].iloc[0]
    ticket = df["ticket"].iloc[0]
    symbol = df["symbol"].iloc[0]
    volume = df["volume"].iloc[0]
    
    # Passing the data to the method
    conn.close_position(symbol,ticket,type_ord,volume,"Trade closed from my code")  

## get_data(symbol, temp, n_periods, plot=0)

### Parameters

<ol>
    <li>symbol:Name of the symbol --> str</li>
    <li>temp: TimeFrame to get data (M1,M3,H1) --> str </li>
    <li>n_periods: Number of candles to get from current time (Current time - n_periods) --> int </li>
    <li>plot: Display a chart in japanese format (1 - Display) --> int </li>
</ol>

### Example:
    
Return a dataFrame with the last 100 min and plot it.
    
    data_from_n_periods = MT5.get_data("EURUSD","M1",100,1)      

To check the correct timeframes print the next code:

    print(MT5.timeframes)

In this example the name of the stock was manually passed, remember use the aproppiate method to extract the name exactly as the broker to avoid errors.
</p>

## calculate_profit(symbol,points,lot,order)

### Parameters

<ol>
    <li>symbol:Name of the symbol --> str</li>
    <li>points: Number of points to calculate the profit/loss --> int </li>
    <li>lots: Size of the simulated trade --> float/int </li>
    <li>order: BUY (1) or SELL (0) --> int </li>
</ol>

<p>This method allow you to calculte the profit or loss without need to open trades.

### Examples
<b>Profit from a trade in EURUSD symbol</b>
   
    profit = MT5.calculate_profit("EURUSD",40,0.1,0)
    


# Technical Class
Contains multiple types of technical analysis, it is based in TA-Lib and modified for personal use with extra features.

To know more information about the functions of TA-Lib, please refer the next documentation:
https://mrjbq7.github.io/ta-lib/index.html


## Constructor method

To start applying technical analysis an object with a dataFrame needs to be created, you can passed any pandas dataFrame that follow the same format as the [get_data](#get_datasymbol-temp-n_periods-plot0) method from the [MT5 Class](#mt5-class).


### Example: 
        
    Technical =  Technical(df)

## get_bars_direction(lenght)

### Parameters
<ol>
    <li>lenght: Number of periods to use to determine the trend. -- > int</li>
</ol>

Determine the direction of each bar from the dataFrame based on the open and close price and return a list.

### Example:

    # Get the direction from the last 50 bars
    trend = Technical.get_bar_direction(50)

## EMA(entry = "close", period = 12, deviation=-1)

Calculate the values for an exponential moving average, by default is set up to 12 periods and  it is based in close price.

### Parameters

<ol>
    <li>entry: Column to perform calculation values. --> str</li>
    <li>period: Number of periods to perform the calculation. --> int </li>
    <li>deviation: Offset used to perfomr calculation --> int </li>    
</ol>


### Example: 
        
    EMA = Technical.EMA("open","100")

## SMA(entry = "close", period = 12, deviation=-1)

Calculate the values for a simple moving average, by default is set up to 12 periods and  it is based in close price.

### Parameters

<ol>
    <li>entry: Column to perform calculation values. --> str</li>
    <li>period: Number of periods to perform the calculation. --> int </li>
    <li>deviation: Offset used to perfomr calculation --> int </li>    
</ol>


### Example: 
        
    SMA = Technical.SMA("open","100")

## calculate_middle_price(period=10)

### Parameters
<ul>
     <li>period: Number of periods to perform the calculation. --> int </li>
</ul>

### Example:

    middle_price = Technical.calculate_middle_price(20)

## calculate_roc(entry="open", period=8)

### Parameters
<ul>
     <li>period: Number of periods to perform the calculation. --> int </li>
</ul>

### Example:

    roc = Technical.calculate_roc("close",20)

## calculate_avg_price()

Calculates the average price for all the time in the dataFrame passed when the object was created.

### Example:

    avg_price = Technical.calculate_avg_price()

## get_previous_bar_trend()

Return the trend from the previous bar based in open and close values.

### Example

    previous_bar_direction = Technical.get_previous_bar_trend()

## get_current_bar_trend()

Return the current trend from the current bar based in open and close values.

### Example

    current_bar_direction = Technical.get_current_bar_trend()

## calculate_trend_by_bars_trend(n_periods=0)

### Parameters
<ul>
    <li>n_periods: Number of periods used to determine trend. --> int </li>
</ul>

Determine the trend based on the direction of each bar for the selected window of periods. 

<i>Note: By default (0) takes all available bars.</i>

### Example

    trend = Technical.calculate_trend_by_bars_trend()

## calculate_trend_by_trendline(n_periods=0)

### Parameters
<ul>
    <li>n_periods: Number of periods used to determine trend. --> int </li>
</ul>

Determine the trend tracing a line from the first and last bar for the window of period selected. 

<i>Note: By default (0) takes all available bars.</i>

### Example

    trend = Technical.calculate_trend_by_trendline()

## calculate_chopiness_index(lookback=6)

### Parameters
<ul>
    <li>lookback: Number of periods to rolling. --> int</li>    
</ul>

Calculate the Chopiness Index value for each period of time to determine when market is on trending.

### Example

    chop = Technical.calculate_chopiness_index(12)

## calculate_trend_angle(n_periods=50)

### Parameters
<ul>
    <li>n_periods: Number of periods used to calculate the angle. --> int </li>
</ul>

 Calculate the angle of the current trend from the selected window of time.
### Example:

    angle = Technical.calculate_trend_angle(20)

 ## get_lowest_and_highest(lenght=10)

 ### Parameters
<ul>
    <li>lenght: Number of periods used to get values. --> int </li>
</ul>

 Calculate the lowest and highest values for a window of time.

### Example:

    lowest, highest = Technical.get_lowest_and_highest(30)

## calculate_super_trend(atr_period=15, multiplier=3)

### Parameters
<ol>
<li>atr_period: Number of periods to take to perform the ATR calculation --> int</li>
<li>multiplier: Multiplier to take to perform the calculation --> float</li>
</ol>

 Calculate super trend indicator values and return the direction.

### Example:

    trend_by_super_trend = Technical.calculate_super_trend(10,.5)








