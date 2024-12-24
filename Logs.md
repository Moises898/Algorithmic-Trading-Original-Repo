## Startegy Description

The strategy is based in EMA crossing with extra confrimations such as:

<li>Chopiness Index in trending (>= 38.1)</li>
<li>Supertrend direction is different from current bar trend</li>
<li>Cross over and Cross under with the central EMA determine the entry</li>
<li>Signal to open needs to be at least 30 % of the last trend (prevents to open in wrong direction with strong trends)</li>

## Additional Features

The strategy can be runned with multiple configuration such as:

<li>TRAILLING STOP: Monitor the price and update the SL and TP every 20 % of total distance from entry price to TP.</li>
<li>FIBONNACI TRAILLING STOP: Monitor the price and set intermidiate SL/TP in fibonnaci levels.</li>
<li>PARTIAL CLOSE: An entry is closed when the price reach one of the levels of the previous monitor functions.</li>
<li>ENTRIES PER SIGNAl: Number of trades to open per signal detected.</li>
<li>AUTOMATIC POINTS: SL and TP are calculated in Fibonnaci levels distance.</li>
<li>RANDOM FOREST: Random Forest model used to determine if the signal detected is accurate or not.</li>

## ML Model

A random forest was trained due was the one with better accuracy, I already tried different aproach embedding a base model and combining with a model trained with current data, the result still changin and didn't get the expected results.

It can enabled or not to reverse the entries if the prediction doesn't match.

## Last implementation

The random forest is enbled, if the prediction don't match a trendline will be traced to see the trend and this will decide the operation type.

## Update 19/09/2024

The main idea from the code it was to execute one trade at the time and analyze when to close it, after a couple of month seems to be not profitable and based on the backtest module, the strategy seems to be profitable if the signals are opened and leave them to close as theirself, the ratio of this is based 1:2 and present profit in most cases with 400 points for XAUUSD, code will be refactor to clean the code and execute in this ways with a time-interval of 10 min as default between trades.

The strategy will open the trades based on the signals until a max number of trades will be opened.

## Update 29/09/2024

Start cleaning and adding documentation from scracth to the code.

MT5 and Technical Classes already cleaned, add a new file called live_trading where I want to implement a method to call from the GUI and easily apply the parameters passed.

## Update 23/10/2024

Modify on tick and ema_crossinf fucntion to fix the current problem related with the time, need to be tested.

Key argument was implemented in different way in order to simplify the logic.

## 28/10/2024

Live trading multiple trades semi working for dynamic points, update the static points to work in the same way.
- Fix the multiple threads, when the first interval of time is reached the new interval is not working, causing open multiple entries and reaching the max.
- Optimize rest of the modules.
- Work in generate a Q1 performance.

## 14/12/2024

GUI updated according new live_trading functions

# Pending Functions

Automatic optimization: Execute this function automatically every certain interval. Function will execute a backtest and adjust parameters based on these.
