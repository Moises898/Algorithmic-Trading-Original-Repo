import talib as ta
from math import atan2, pi
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def direction(bar):
    if bar["open"] < bar["close"]:
        # Bullish bar
        direction = 1
    elif bar["open"] > bar["close"]:
        # Bearish bar
        direction = 0
    else:
        # Doji bar
        direction = 2

    return direction


class Technical:

    # Construct method that receive the df
    def __init__(self, df=None):
        self.df = df
        self.PREVIOUS_BAR()
        self.CURRENT_BAR()
        self.df = self.df.copy()
        self.df["hl2"] = (self.df["high"]+self.df["low"])/2

    # Return the direction of each bar
    def RETURN_DIRECTION(self, lenght):
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

    # Exponential Moving Averge indicator
    def EMA(self, entry="close", period=12,deviation=-1):
        df = self.df
        ema = ta.EMA(df[entry], timeperiod=period)
        if deviation > 0:            
            ema = ema[:-deviation]
        return ema

    # Simple Moving Averge indicator
    def SMA(self, entry="close", period=12,deviation=-1):
        df = self.df
        ema = ta.SMA(df[entry], timeperiod=period)
        if deviation > 0:            
            ema = ema[:-deviation]
        return ema
        
    # Calculate middle price in the selected period
    def MIDDLE_PRICE(self, period=10):
        df = self.df
        price = ta.MIDPRICE(df["high"], df["low"], timeperiod=period)
        return price[-1]

    # Calculate the rate of change in the price
    def RATE_OF_CHANGE(self, entry="open", period=8):
        df = self.df
        ROC = ta.ROCP(df[entry], timeperiod=period)
        return ROC

    # AVG-PRICE for the current bar
    def AVG_PRICE(self):
        df = self.df
        price = ta.AVGPRICE(df["open"], df["high"], df["low"], df["close"])
        return price[-1]

    # Define direction of the previous bar and set LOW and HIGH parameters
    def PREVIOUS_BAR(self):
        df = self.df
        PREV_BAR = df.iloc[-2]
        PREV_BAR_2 = df.iloc[-3]
        self.PREV_BAR_HIGH = PREV_BAR["high"]
        self.PREV_BAR_LOW = PREV_BAR["low"]
        self.PREV_BAR_CLOSE = PREV_BAR["close"]
        self.PREV_BAR_MEDIAN_PRICE = ta.MEDPRICE(
            df["high"], df["low"]).iloc[-1]
        self.PREV_BAR_OPEN = PREV_BAR["open"]
        self.PREV_DIRECTION = direction(PREV_BAR)
        self.PREV_DIRECTION_2 = direction(PREV_BAR_2)
        self.PREV_BODY = PREV_BAR["close"] - \
            PREV_BAR["open"] if self.PREV_DIRECTION == 1 else PREV_BAR["open"] - \
            PREV_BAR["close"]
        # BUY
        if self.PREV_DIRECTION == 1:
            self.MECHA_SUPERIOR = self.PREV_BAR_HIGH - self.PREV_BAR_CLOSE
            self.MECHA_INFERIOR = self.PREV_BAR_OPEN - self.PREV_BAR_LOW
        # SELL
        elif self.PREV_DIRECTION == 0:
            self.MECHA_SUPERIOR = self.PREV_BAR_HIGH - self.PREV_BAR_OPEN
            self.MECHA_INFERIOR = self.PREV_BAR_CLOSE - self.PREV_BAR_LOW
        else:
            self.MECHA_SUPERIOR = 1
            self.MECHA_INFERIOR = 1
        return self.PREV_DIRECTION

    # Define direction of the previous bar and set LOW and HIGH parameters
    def CURRENT_BAR(self):
        df = self.df
        CURRENT_BAR = df.iloc[- 1]
        self.CURR_BAR_HIGH = CURRENT_BAR["high"]
        self.CURR_BAR_LOW = CURRENT_BAR["low"]
        self.CURR_BAR_CLOSE = CURRENT_BAR["close"]
        self.CURR_BAR_OPEN = CURRENT_BAR["open"]
        self.CURR_BAR_MEDIAN_PRICE = ta.MEDPRICE(
            df["high"], df["low"]).iloc[-1]
        self.CURR_DIRECTION = direction(CURRENT_BAR)
        self.CURR_BODY = CURRENT_BAR["close"] - \
            CURRENT_BAR["open"] if self.CURR_DIRECTION == 1 else CURRENT_BAR["open"] - \
            CURRENT_BAR["close"]
        # BUY
        if self.CURR_DIRECTION == 1:
            self.MECHA_SUPERIOR_CURR = self.CURR_BAR_HIGH - self.CURR_BAR_CLOSE
            self.MECHA_INFERIOR_CURR = self.CURR_BAR_OPEN - self.CURR_BAR_LOW
        # SELL
        elif self.CURR_DIRECTION == 0:
            self.MECHA_SUPERIOR_CURR = self.CURR_BAR_HIGH - self.CURR_BAR_OPEN
            self.MECHA_INFERIOR_CURR = self.CURR_BAR_CLOSE - self.CURR_BAR_LOW
        else:
            self.MECHA_SUPERIOR_CURR = 1
            self.MECHA_INFERIOR_CURR = 1

        return self.CURR_DIRECTION

    # Count the direction of each bar to determine the trend
    def TREND_BY_BARS_DIRECTION(self, index=0):
        df = self.df
        trend_counters = {
            "bullish_counter": 0,
            "bearish_counter": 0,
            "doji_counter": 0
        }
        # Loop to calculate the direction of each bar
        for bar in range(len(df.iloc[index:])):
            dir = direction(df.iloc[index+bar])
            if dir == 1:
                trend_counters["bullish_counter"] = trend_counters["bullish_counter"] + 1
            elif dir == 0:
                trend_counters["bearish_counter"] = trend_counters["bearish_counter"] + 1
            else:
                trend_counters["doji_counter"] = trend_counters["doji_counter"] + 1
        # Define main trend
        if trend_counters["bearish_counter"] > trend_counters["bullish_counter"]:
            # Bearish trend
            trend = 0
        elif trend_counters["bearish_counter"] < trend_counters["bullish_counter"]:
            # Bullish trend
            trend = 1
        else:
            # No dominant trend
            trend = 2
        return trend

    # Compare the first bar with the last to determine the trend
    def TREND_BY_TRENDLINE(self, index=0):
        df = self.df
        # Define main trend
        if df["close"].iloc[index] > df["close"].iloc[-1]:
            # SELL
            trend = 0
        elif df["close"].iloc[index] < df["close"].iloc[-1]:
            # BUY
            trend = 1
        else:
            # Same entry
            trend = 2
        return trend

    # Choppiness  Index
    def CHOP(self, lookback=6, deviation=-1):
        """
            IF CHOPPINESS INDEX <= 38.2 --> MARKET IS TRENDING
        """
        df = self.df
        tr1 = pd.DataFrame(df["high"] - df["low"]).rename(columns={0: 'tr1'})
        tr2 = pd.DataFrame(
            abs(df["high"] - df["close"].shift(1))).rename(columns={0: 'tr2'})
        tr3 = pd.DataFrame(
            abs(df["low"] - df["close"].shift(1))).rename(columns={0: 'tr3'})
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join='inner').dropna().max(axis=1)
        atr = tr.rolling(1).mean()
        highh = df["high"].rolling(lookback).max()
        lowl = df["low"].rolling(lookback).min()
        ci = 100 * np.log10((atr.rolling(lookback).sum()) /
                            (highh - lowl)) / np.log10(lookback)            
        return ci.iloc[deviation] 

    # Trend Angle
    def TREND_ANGLE(self, index=0):
        df = self.df
        df = df.iloc[index:]
        df.reset_index(inplace=True)
        Y1 = df["close"].iloc[0]
        Y2 = df["close"].iloc[len(df)-1]
        ANGLE = atan2((Y2 - Y1), 0.10) * 180 / pi
        return ANGLE

    # Lowest and highest values from the window passed
    def LOWEST_AND_HIGHEST(self, lenght=10):
        df = self.df        
        highest_high = ta.MAX(df["high"], timeperiod=lenght)
        lowest_low = ta.MIN(df["low"], timeperiod=lenght)        
        return lowest_low[-1],highest_high[-1]    

    # SUPER TREND FUNCTION THAT RETURN DIRECTION OF SIGNAL
    def SUPER_TREND(self, atr_period=15, multiplier=3):
        df = self.df
        high = df['high']
        low = df['low']
        close = df['close']

        atr = ta.ATR(high, low, close, atr_period)
        hl2 = (high + low) / 2
        final_upperband = upperband = hl2 + (multiplier * atr)
        final_lowerband = lowerband = hl2 - (multiplier * atr)

        supertrend = [True] * len(df)

        for i in range(1, len(df.index)):
            curr, prev = i, i-1
            # if current close price crosses above upperband
            if close[curr] > final_upperband[prev]:
                supertrend[curr] = True
            # if current close price crosses below lowerband
            elif close[curr] < final_lowerband[prev]:
                supertrend[curr] = False
            # else, the trend continues
            else:
                supertrend[curr] = supertrend[prev]
                # adjustment to the final bands
                if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                    final_lowerband[curr] = final_lowerband[prev]
                if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                    final_upperband[curr] = final_upperband[prev]

            # to remove bands according to the trend direction
            if supertrend[curr] == True:
                final_upperband[curr] = np.nan
            else:
                final_lowerband[curr] = np.nan
        
        return 1 if supertrend[-1] else 0
    
    def HT_TRENDLINE(self):
        df = self.df
        HT = ta.HT_TRENDLINE(df["close"].values)
        return HT[-1]
