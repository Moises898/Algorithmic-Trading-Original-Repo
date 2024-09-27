## Startegy Description

The strategy have 2 ways two run:

1. Strategy using Fibonnacci SL/TP points, once the strategy detects an entry the SL and TP are set up based on fibonacci levels, in this way the SL and TP are dynamic and numeber of pips will depend on current market conditions.w
The ratio beetween SL and TP also follows a 1:2 rule meaning that unless the accruracy of the entries is lower we can get profit in long-term.

2. Default points. the strategie detects entries and SL/TP are set up in the same distance, accuracy needs to be greater to allow a profit in long term.

<i>Note: For both options a stip trailling could be enabled menaing the positions moving in the rigth trend could be closed before reach the TP</i>

## ML Model

A random forest was trained due was the one with better accuracy, I already tired different aproach embedding a base model and combining with a model trained with current data, the result still changin and didn't get the expected results.

It can enabled or not to reverse the entries if the prediction doesn't match.

## Last implementation

The random forest is enbled, if the prediction don't match a trendline will be traced to see the trend and this will decide the operation type.

## Update 19/09/2024

The main idea from the code it was to execute one trade at the time and analyze when to close it, after a couple of month seems to be not profitable and based on the backtest module, the strategy seems to be profitable if the signals are opened and leave them to close as theirself, the ratio of this is based 1:2 and present profit in most cases with 400 points for XAUUSD, code will be refactor to clean the code and execute in this ways with a time-interval of 10 min as default between trades.

The strategy will open the trades based on the signals until a max number of trades will be opened.