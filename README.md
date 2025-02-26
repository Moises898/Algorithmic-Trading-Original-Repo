
- [Installation](#installation)
- [Introduction](#introduction)
- [MT5](#mt5)
  - [Constructor Method](#constructor-method)
    - [Parameters](#parameters)
    - [Example:](#example)
  - [start()](#start)
    - [Example:](#example-1)
  - [close()](#close)
    - [Example:](#example-2)
  - [account\_details(show=0)](#account_detailsshow0)
    - [Example:](#example-3)
  - [display\_symbols(keyword,spread=30)](#display_symbolskeywordspread30)
    - [Parameters](#parameters-1)
    - [Example:](#example-4)
  - [open\_position(symbol,operation,lot,points=40,comment="Python")](#open_positionsymboloperationlotpoints40commentpython)
    - [Parameters](#parameters-2)
    - [Example:](#example-5)
  - [get\_positions(symbol=None)](#get_positionssymbolnone)
    - [Parameters](#parameters-3)
    - [Example:](#example-6)
  - [close\_position(ticket, comment="Close", display=False)](#close_positionticket-commentclose-displayfalse)
    - [Parameters](#parameters-4)
    - [Examples:](#examples)
  - [get\_data(symbol, temp, n\_periods, plot=0)](#get_datasymbol-temp-n_periods-plot0)
    - [Parameters](#parameters-5)
    - [Example:](#example-7)
  - [calculate\_profit(symbol,points,lot,order)](#calculate_profitsymbolpointslotorder)
    - [Parameters](#parameters-6)
    - [Examples](#examples-1)


# Installation

1. Clone the repository to your local machine
2. Create a virtual env to avoid issues between versions using `python -m venv name_env`
3. Activate virtual env and run `pip install -r requirements.txt`
4. Go to the examples section and modify the .env file with your own data to start interacting with MT5.

<i>Note: You need to have a terminal of Metatrader 5 in your computer to work.</i>

# Introduction
<p>This module use the Metatatrader5 library to connect with the platform, the functions were adapted to launch operations with own parameters and conditions.To know more information about the functions of Metatrade 5, please refer the next documentation:<br> 
https://www.mql5.com/en/docs/integration/python_metatrader5 </p>

<p>Next you can read more about each function and how to implement it.</p>

# MT5

This class is a wrapper for the MT5 library that contains all related methods to interact with Metatrader 5 such as: 

<li>Create Connection</li>
<li>Retrieve data</li>
<li>Open Trades</li>
<li>Close Trades</li>
<li>Get Account Info</li>

## Constructor Method

<p>Create an object to enable the connection with MT5

### Parameters
<ol>
<li>User (int) --> Account Id</li>
<li>Password (str) --> Password of the Account</li>
<li>Server (str) --> Server of the Account</li>
</ol>

### Example:
    
    user = 12345
    password = "passwd123"
    server = "MetaQuotes-Demo"
    conn = MT5(user,password,server)

<i>Note: By default the contructor method call the start method to start the connection to the MT5 server which will open the terminal of MT5.</i>
</p>


## start()
<p>Create a connection to the Metatrader 5 server.<br>

### Example:
    
    conn.start()
</p>


## close()
<p>Close the connection to Metatrader5 server.<br>

### Example:
        
    conn.close()
</p>



## account_details(show=0)
<p>Return an object of type AccountInfo from Metatrader 5 library that contains all the information related to the account. <br>

<i>Note: If you want to print the info pass 1 as and argument.</i><br>

### Example:

    # Display object with attributes
    conn.account_details(1)
<br>

    # Save balance into a variable
    balance = conn.account_details().balance

</p>

## display_symbols(keyword,spread=30)

### Parameters
<ol>
    <li>keyword (list) --> Keywords to match the symbols.</li>
    <li>spread (int) --> Maximum value of spread of the symbols.</li>
</ol>

<p>The method will return a DataFrame with most relevant data of the symbols that satisfy the criteria.. <br>


### Example:
    
    # Filter the symbols that contains "EUR" or "USD" and the spread value is less than 30
    symbols = conn.display_symbols(["EUR","USD"],30)    
</p>


## open_position(symbol,operation,lot,points=40,comment="Python")

### Parameters

<ol>
    <li>symbol (str) --> Name of the symbol exactly as in the broker appears</li>
    <li>operation (int) --> BUY(1) / SELL(0) </li>
    <li>lot (int) --> Size of the operation to open </li>
    <li>points (int) or (list)</li>
        <ul>a) Number of points to set the SL and TP from the entry price. This will follow 1:1 ratio.</ul>
        <ul>b) [SL,TP] a list with the specific values of the price where the SL and TP should be set.</ul>
    <li>comment: Comment displayed in the MT5 console.</li>
</ol>
<br>

<p>This method create and send a request to execute the position with the input parameters.<br>

<i><b>Note: Use the display_symbols() to retrive the right name of the symbol.</b></i></p>


### Example: 

<b>SELL 0.2 lots in EURUSD with 40 points as SL/TP</b>

    order_id = conn.open_position("EURUSD",0,0.2,40,"This trade was executed from my code")    
</p>

## get_positions(symbol=None)

### Parameters

<ol>    
    <li>symbol (str) --> Get trades info exclusively of the symbol passed </li>    
</ol>

<p>Returns a pandas dataframe with trades open if exists.
<br>

### Example: 

    df = conn.get_positions()   
</p>

## close_position(ticket, comment="Close", display=False)

### Parameters

<ol>    
    <li>ticket (int) --> Ticket number of the trade to close </li>   
    <li>comment (str) --> Comment to add to the order.</li>
</ol>

<p>This method create and send the request to close the position with passed args.<br>


### Examples:
       
    
    ticket_id = 12345

    conn.close_position(ticket_id,"Trade closed from my code")  

## get_data(symbol, temp, n_periods, plot=0)

### Parameters

<ol>
    <li>symbo (str) --> Name of the symbol</li>
    <li>temp (str) --> TimeFrame to get data (M1,M3,H1, etc)</li>
    <li>n_periods (int) --> Number of bars to get from current time (Current time - n_periods)</li>
    <li>plot (int) --> Display a chart in japanese format 
    <ul>1 - Plot the DataFrame</ul>
    <ul>0 - Only returns the DataFrame (default) </ul>
    </li>
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