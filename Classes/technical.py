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

    # Constructor method that receive the df
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
        self.df["hl2"] = (self.df["high"] + self.df["low"]) / 2

    # Return the direction of each bar
    def get_bars_direction(self, lenght):
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

    # Exponential Moving Averge indicator
    def EMA(self, entry="close", period=12, deviation=-1):
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

    # Simple Moving Averge indicator
    def SMA(self, entry="close", period=12, deviation=-1):
        """
        Calculate a Simple Moving Average based on the args passed.

        Args:
            entry (str, optional): Column to use to calculate the SMA . Defaults is to "close".
            period (int, optional): Number of periods to calculate the SMA . Defaults is to 12.
            deviation (int, optional): Offset the values to get a deviation of n_periods. Defaults to -1.

        Returns:
            list : List of the the values for each time of period of the dataFrame.
        """
        df = self.df
        sma = ta.SMA(df[entry], timeperiod=period)
        if deviation > 0:
            sma = sma[:-deviation]
        return sma

    # Calculate middle price in the selected period
    def calculate_middle_price(self, period=10):
        """
        Calculate the middle price for the selected window of periods.

        Args:
            period (int, optional): Number of periods to calculate the middle price. Defaults to 10.

        Returns:
            list : List of middle prices for each time of period of the dataFrame.
        """
        df = self.df
        price = ta.MIDPRICE(df["high"], df["low"], timeperiod=period)
        return price

    # Calculate the rate of change in the price
    def calculate_roc(self, entry="open", period=8):
        """
        Calculate the rate of change (ROC) for the selected window of periods.

        Args:
            entry (str, optional): Column to use to calculate the ROC values. Defaults to "open".
            period (int, optional): Number of period to perfom the calculation. Defaults to 8.

        Returns:
            list: List of ROC values for each time of period of the dataFrame.
        """
        df = self.df
        ROC = ta.ROCP(df[entry], timeperiod=period)
        return ROC

    # AVG-PRICE 
    def calculate_avg_price(self):
        """
        Calculate the average price.

        Returns:
            list : Return a list with the average prices for each time of period of the dataFrame.
        """
        df = self.df
        price = ta.AVGPRICE(df["open"], df["high"], df["low"], df["close"])
        return price

    # Define direction of the previous bar and set LOW and HIGH parameters
    def get_previous_bar_trend(self):
        """
        Get previous bar trend based in open and close values.

        Returns:
            int : Uptrend (1) or Downtrend (0)
        """
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
    def get_current_bar_trend(self):
        """
        Get current bar trend based in open and close values.

        Returns:
            int : Uptrend (1) or Downtrend (0)
        """
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
    def calculate_trend_by_bars_trend(self, n_periods=0):
        """
        Calculate the trend based on each bar direction for the selected window of periods.

        Args:
            n_periods (int, optional): Number of period to perform the calculation . Defaults to 0.

        Returns:
            int :  Uptrend (1) or Downtrend (0)
        """
        df = self.df
        trend_counters = {
            "bullish_counter": 0,
            "bearish_counter": 0,
            "doji_counter": 0
        }
        # Loop to calculate the direction of each bar
        for bar in range(len(df.iloc[-n_periods:])):
            dir = direction(df.iloc[-n_periods + bar])
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
    def calculate_trend_by_trendline(self, n_periods=0):
        """
        Calculate the trend based on a trend line from for the selected window of periods. Close values are used to calculate the trendline.

        Args:
            n_periods (int, optional): Number of period to perform the calculation. Defaults to 0.

        Returns:
            int :  Uptrend (1) or Downtrend (0)
        """
        df = self.df
        # Define main trend
        if df["close"].iloc[-n_periods] > df["close"].iloc[-1]:
            # SELL
            trend = 0
        elif df["close"].iloc[-n_periods] < df["close"].iloc[-1]:
            # BUY
            trend = 1
        else:
            # Same entry
            trend = 2
        return trend

    # Choppiness  Index
    def calculate_chopiness_index(self, lookback=6):
        """
        Calculate the chopiness index values.

        Args:
            lookback (int, optional): Number of periods to rolling. Defaults to 6.

        Returns:
            list : CHOP values for each period of time.
        
        Note:
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
        return ci

        # Trend Angle

    def calculate_trend_angle(self, n_periods=50):
        """
        Calculate the angle of the current trend from the selected window of time.

        Args:
            n_periods (int, optional): Number of periods to take to perform the calculation. Defaults to 50.

        Returns:
            float : Angle of th trend from first to current bar.
        """
        df = self.df
        # If the n_periods is lower than the lenght of the dataFrame
        if not n_periods > df.shape[0]:
            df = df.iloc[-n_periods:]
            df.reset_index(inplace=True)
        Y1 = df["close"].iloc[0]
        Y2 = df["close"].iloc[len(df) - 1]
        ANGLE = atan2((Y2 - Y1), 0.10) * 180 / pi
        return ANGLE

    # Lowest and highest values from the window passed
    def get_lowest_and_highest(self, lenght=10):
        """
        Calculate the lowest and highest values for a window of time.

        Args:
            lenght (int, optional): Number of periods to take to perform the calculation. Defaults to 10.

        Returns:
            float, float : Lowest and Highest values
        """
        df = self.df
        highest_high = ta.MAX(df["high"], timeperiod=lenght)
        lowest_low = ta.MIN(df["low"], timeperiod=lenght)
        return lowest_low[-1], highest_high[-1]

        # SUPER TREND FUNCTION THAT RETURN DIRECTION OF SIGNAL

    def calculate_super_trend(self, atr_period=15, multiplier=3):
        """
        Calculate super trend indicator values and return the direction.

        Args:
            atr_period (int, optional): Number of periods to take to perform the ATR calculation. Defaults to 15.
            multiplier (float, optional): Multiplier to take to perform the calculation. Defaults to 3.

        Returns:
            int : Uptrend (1) or Downtrend (0)
        """
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
            curr, prev = i, i - 1
            # if current close price crosses above upper band
            if close[curr] > final_upperband[prev]:
                supertrend[curr] = True
            # if current close price crosses below lower band
            elif close[curr] < final_lowerband[prev]:
                supertrend[curr] = False
            # else, the trend continues
            else:
                supertrend[curr] = supertrend[prev]
                # adjustment to the final bands
                if supertrend[curr] and final_lowerband[curr] < final_lowerband[prev]:
                    final_lowerband[curr] = final_lowerband[prev]
                if not supertrend[curr] and final_upperband[curr] > final_upperband[prev]:
                    final_upperband[curr] = final_upperband[prev]

            # to remove bands according to the trend direction
            if supertrend[curr]:
                final_upperband[curr] = np.nan
            else:
                final_lowerband[curr] = np.nan

        return 1 if supertrend[-1] else 0
