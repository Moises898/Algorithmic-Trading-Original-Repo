# ATLAS Algorithmic Trading

<h2>Introduction</h2>
<p>This module use the Metatatrader5 library to connect with the platform, the functions were adapted to launch operations with own parameters and conditions.To know more information about the functions of Metatrade5, please refer the next documentation:<br> 
https://www.mql5.com/en/docs/integration/python_metatrader5 </p>

<p>Next you can read more about each function and how to implement it.</p>



# MT5 Class

All related methods for request retrieve and send data with the platform of Metatrader 5.

<h3><b> Constructor Method</b></h3>
<p>Every time we instanciate a new object of this class the cosntructor method is called and needs to receive 3 parameters:
<ol>
<li>User (int type)</li>
<li>Password (str type)</li>
<li>Server (str type)</li>
</ol>

Example: <br>
    
    user = 12345
    password = "passwd123"
    server = "MetaQuotes-Demo"
    conn = MT5(user,password,server)

</p>



<h3><b> start()</b></h3>
<p>Call this method once we create our object to stablish the connection with Metatrader5.<br>

Example: <br>
    
    conn.start()
</p>


<h3><b> close()</b></h3>
<p>Call this method at the end of your code to close the connection to Metatrader5.<br>

Example: <br>
        
    conn.close()
</p>



<h3><b> account()</b></h3>
<p>Display most important information from your account, this method return the balance.<br>

Example: <br>
    
    #Display only the info
    conn.account()
    
    #Display and set the value to a variable
    balance = conn.account()

</p>



<h3><b> display_symbols(elements,sprd=10)</b></h3>
<p>Use this method to filter and display only the actives symbols with spread less than the input and contains the keyword passed. 
This method by default filter spread less than 10 and return a list with the symbols information.<br>

Example: <br>
    
    #Filter the symbols that contains "EUR" and spread less than 5 
    symbols = conn.display_symbols(["EUR"],5)    
</p>


<h3><b> open_position(symbol,operation,lot,points=40,comment="Python") </b></h3>
<p>This method create and send a request to execute the position with the input parameters.<br>
<ol>
<li>symbol: Name of the symbol exactly as the broker provided.</li>
<li>operation: BUY(1), SELL(0)</li>
<li>lot: Size of the operation to open.</li>
<li>points:</li>
<ul>a) Number of points to set the SL and TP from the entry poitnt, points are calculated automatically based on the symbol.</ul>
<ul>b) [SL,TP] a list with the specific price where the SL and TP should be set.</ul>
<li>comment: Comment displayed in the MT5 console.</li>
</ol>
<br>

<i><b>Note: Use the display_symbols() to retrive the name and pass it correctly.</b></i>
<br>
<br>
Example: 

<b>SELL 0.2 lots EURUSD with 40 points as SL/TP</b>

    order_id = conn.open_position("EURUSD",0,0.2,40,"This trade was executed from my code")    
</p>

<h3><b> get_positions() </b></h3>
<p>Returns a pandas dataframe with trades open if exists.
<br>
Example: 

    df = conn.get_positions()   
</p>

<h3><b> close_position(stock,ticket,type_order) </b></h3>
<p>This method create and send the request to close the position with the passed parameters.<br>
To get the required paramateres we can use the get_positions() method and select one of the current open positions from the dataFrame.
<br>

<b>Assigning the values from the columns to variables</b>
   
    df = conn.get_positions()
    type_ord = df["type"].iloc[0]
    ticket = df["ticket"].iloc[0]
    symbol = df["symbol"].iloc[0]
    
    # Passing the data to the method
    conn.close_position(symbol,ticket,type_ord)  

<h3><b> data_range(symbol, temp, hours, plot=0)</b></h3>

<p>This method retrive the data in format of dataFrame from the period and temporary passed.<br>
The method will return the informartion from the current time less the hours selected in the timeframe passed.<br>
<br>
<i><b>Note: By default the method doesn't return a graph if you want to plot it pass 1 as parameter at the end.</b></i>

Example: <br>
    
Return a dataFrame with 100 min ago to current time and plot it
    
    ranges = MT5.data_range("EURUSD","M1",100,1)      

To check the correct timeframes print the next code:

    print(MT5.timeframes)

In this example the name of the stock was manually passed, remember use the aproppiate method to extract the name exactly as the broker to avoid errors.
</p>

<h3><b> calculate_profit(symbol,points,lot,order) </b></h3>
<p>This method allow you to calculte the profit or loss without need to open trades.<br>
<br>
<b>Profit from a trade in EURUSD </b>
   
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






