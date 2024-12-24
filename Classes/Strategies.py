from Classes.data_operations import CROSSING
from Classes.technical import Technical
from Classes.randomForest import inputs_for_random_forest,get_prediction,inputs_for_random_forest_v2

# Parameteters for strategy (not modify)
PARAMETERS = lambda x: {    
        "OFFSET": 2,
        "CHOP_LIMIT": 50.24,
        "CHOP_LENGHT": 4,
        "ATR_LENGHT": 15,
        "FACTOR": 2.4,
        "EMA_OPEN": 4,
        "EMA_LH": 4 if x == "XAUUSD" else 2
    }

def EMA_CROSSING(df,offset=3, ema_open=15, ema_period=3,reverse=False,show=False):
    """
    Description:
        The strategy looks for crossing between the upper and lower EMA with the central one. 
        - CHOP Index < 50.
        - Supertrend Direction is opposite to the signal detected by EMA Crossing.
        - Trend of last 30 times is at least 35 % of signal detected. If not open in main trend     
    Additional:
        - Volume Filter: Volume increase from previous bar. (If not signal skipped)       

    Args:
        df (pandas dataframe): Data used to check for entries
        offset (int, optional): _description_. Defaults to 3.
        ema_open (int, optional): _description_. Defaults to 15.
        ema_period (int, optional): _description_. Defaults to 3.
        reverse (bool, optional): _description_. Defaults to False.
        volume_filter (bool, optional): Extra Filter, If volume don't increase signal turns to False . Defaults to False.
        show (bool, optional): Display signal detected to the console. Defaults to False.

    Returns:
        list --> boolean,int: Returns TRUE or FALSE and the trend to open trade
    """
    
    operation = False
    trend_for_operation = 2
    M1_technical = Technical(df)
    counters = M1_technical.get_bars_direction(30)
    chopiness_index = M1_technical.calculate_chopiness_index(PARAMETERS("XAUUSD")["CHOP_LENGHT"])[-1]
    if len(counters) > 2:
        total = 30 - counters[2]
    else:
        total = 30    
    if chopiness_index < PARAMETERS("XAUUSD")["CHOP_LIMIT"]:                
        # Set PARAMETERS         
        EMA_LOW = M1_technical.EMA(entry="low", period=ema_period, deviation=offset)
        EMA_HIGH = M1_technical.EMA(entry="high", period=ema_period, deviation=offset)
        EMA_OPEN = M1_technical.EMA(entry="open", period=ema_open, deviation=-1)
        supertrend = M1_technical.calculate_super_trend(PARAMETERS("XAUUSD")["ATR_LENGHT"], PARAMETERS("XAUUSD")["FACTOR"])          
        if (CROSSING(EMA_OPEN, EMA_HIGH, 0)) and supertrend == 0:            
            # SELL Under
            if counters[-1] / total >= .35:
                if show:
                    print("Sell under")
                operation = True
                trend_for_operation = 0                
            else:
                if show:
                    print("Buy by Strong Trend")
                operation = True
                trend_for_operation = 1                 
        
        elif (CROSSING(EMA_OPEN, EMA_LOW, 1)) and supertrend == 1:
            # BUY Over
            if counters[1] / total >= .35:
                if show:
                    print("Buy over")
                operation = True
                trend_for_operation = 1
            else:
                if show:
                    print("Sell by Strong Trend")
                operation = True
                trend_for_operation = 0                        
        if reverse:
            trend_for_operation = 0 if trend_for_operation == 1 else 1
    return operation, trend_for_operation
