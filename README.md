# ATLAS Algorithmic Trading

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

<h3><b> Constructor Method </b></h3>
<p>Create an object to enable the connection with MT5

<h3>Parameters</h3>
<ol>
<li>User --> int</li>
<li>Password --> str</li>
<li>Server --> str</li>
</ol>

Example: <br>
    
    user = 12345
    password = "passwd123"
    server = "MetaQuotes-Demo"
    conn = MT5(user,password,server)

<i>Note: By default the contructor method call the start method to start the connection to the MT5 server</i>
</p>


<h3><b> start()</b></h3>
<p>Stablish a connection to the Metatrader5 server.<br>

Example: <br>
    
    conn.start()
</p>


<h3><b> close()</b></h3>
<p>Close the connection to Metatrader5 server.<br>

Example: <br>
        
    conn.close()
</p>



<h3><b> account_details(show=0)</b></h3>
<p>Return an object of type AccountInfo from Metatrader5 library. <br>
<i>Note: Method don't display info by default pass 1 as arg to print to the console.</i><br>

Example: <br>

    #Display only the info
    conn.account_details()
<br>

    #Display and save the value to a variable
    balance = conn.account_details()

</p>

<h3><b> display_symbols(elements,spread=10)</b></h3>

<h3>Parameters</h3>
<ol>
<li>elements --> list</li>
<li>spread --> int</li>
</ol>

<p>Display symbols that follows the criteria passed (spread, keyword symbol). <br>

This method by default filter spread less than 10 and return a list with the symbols information.<br>

Example: <br>
    
    #Filter the symbols that contains "EUR" and spread less than 5 
    symbols = conn.display_symbols(["EUR"],5)    
</p>


<h3><b> open_position(symbol,operation,lot,points=40,comment="Python") </b></h3>

<h3>Parameters</h3>

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


Example: 

<b>SELL 0.2 lots in EURUSD with 40 points as SL/TP</b>

    order_id = conn.open_position("EURUSD",0,0.2,40,"This trade was executed from my code")    
</p>

<h3><b> get_positions(show,symbol,id) </b></h3>
<h3>Parameters</h3>

<ol>
<li>show: Display message in the console --> int</li>
<li>symbol: Get trades info with symbol passed --> str</li>
<li>id: Get trade info with the ID passed --> str</li>
</ol>

<p>Returns a pandas dataframe with trades open if exists.
<br>
Example: 

    df = conn.get_positions()   
</p>

<h3><b> close_position(symbol,ticket,type_order) </b></h3>
<h3>Parameters</h3>

<ol>
<li>symbol:Name of the symbol to close the trade --> str</li>
<li>ticket: ID of the trade --> str </li>
<li>type_order: BUY (1) or SELL (0) --> int </li>
<li>vol: Size of the trade --> float </li>
<li>comment: Comment to sent (Close by default) --> str</li>
</ol>

<p>This method create and send the request to close the position with passed args.<br>

To get the required args we can use the get_positions() method and select one of the current open positions from the dataFrame or manually pass.
<br>

<b>Assigning the values from the columns to variables</b>
   
    df = conn.get_positions()
    type_ord = df["type"].iloc[0]
    ticket = df["ticket"].iloc[0]
    symbol = df["symbol"].iloc[0]
    volume = df["volume"].iloc[0]
    
    # Passing the data to the method
    conn.close_position(symbol,ticket,type_ord,volume,"Trade closed from my code")  

<h3><b> get_data(symbol, temp, n_periods, plot=0)</b></h3>

<h3>Parameters</h3>

<ol>
<li>symbol:Name of the symbol --> str</li>
<li>temp: TimeFrame to get data (M1,M3,H1) --> str </li>
<li>n_periods: Number of candles to get from current time (Current time - n_periods) --> int </li>
<li>plot: Display a chart in japanese format (1 - Display) --> int </li>
</ol>
Example: <br>
    
Return a dataFrame with the last 100 min and plot it.
    
    data_from_n_periods = MT5.get_data("EURUSD","M1",100,1)      

To check the correct timeframes print the next code:

    print(MT5.timeframes)

In this example the name of the stock was manually passed, remember use the aproppiate method to extract the name exactly as the broker to avoid errors.
</p>

<h3><b> calculate_profit(symbol,points,lot,order) </b></h3>
<h3>Parameters</h3>

<ol>
<li>symbol:Name of the symbol --> str</li>
<li>points: Number of points to calculate the profit/loss --> int </li>
<li>lots: Size of the simulated trade --> float/int </li>
<li>order: BUY (1) or SELL (0) --> int </li>
</ol>

<p>This method allow you to calculte the profit or loss without need to open trades.<br>
<br>
<b>Profit from a trade in EURUSD symbol</b>
   
    profit = MT5.calculate_profit("EURUSD",40,0.1,0)
    



# Technical
Contains multiple types of technical analysis, it is based in TA-Lib and modified for personal use with extra features.
To know more information about the functions of TA-Lib, please refer the next documentation:
https://mrjbq7.github.io/ta-lib/index.html


<h3><b>Constructor method</b></h3>
<p>To start applying technical analysis an object with a dataFrame needs to be created, you can passed any pandas dataFrame that follow the same format as the MT5.data_range() method.


Example: <br>
        
    Technical =  Technical(df)
</p>


<h3><b>EMA(entry = "close", period = 12, deviation=-1)</b></h3>
<p>Calculate the values for an exponential moving average, by default is set up to 12 periods and  it is based in close price.

Example: <br>
        
    EMA = Technical.EMA("open","100")
</p>






