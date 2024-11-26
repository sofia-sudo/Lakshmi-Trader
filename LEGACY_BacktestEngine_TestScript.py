import pandas as pd
import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
from collections import deque
from io import StringIO

df = pd.read_csv('archive/USD_data.csv', chunksize=10000)
df_chunk = next(df)
df_chunk['Date'] = pd.to_datetime(df_chunk['Date'])
df_chunk.set_index('Date', inplace=True)

with open('archive/USD_data.csv', 'r') as f:
    last_10000_lines = deque(f, maxlen=10000)  # Keep only the last 10,000 lines

# Convert the deque to a pandas DataFrame
data_str = ''.join(last_10000_lines)
df_last_10000 = pd.read_csv(StringIO(data_str), names=['UNIX', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'])
df_last_10000['Date'] = pd.to_datetime(df_last_10000['Date'])
df_last_10000.set_index('Date', inplace=True)

print(len(df_last_10000))

print(df_last_10000.head())

def EMA(array, period):
    # Convert the array to a pandas Series
    series = pd.Series(array)
    return series.ewm(span=period, adjust=False).mean().values

# Custom function to calculate the Relative Strength Index (RSI)
def RSI(array, period):
    # Convert the array to a pandas Series
    series = pd.Series(array)
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return (100 - (100 / (1 + rs))).values

# Strategy using EMA and RSI
class EMARsiStrategy(Strategy):
    short_ema_period = 12  # Short-term EMA
    long_ema_period = 26   # Long-term EMA
    rsi_period = 14        # RSI period

    parameters = {
        'short_ema_period': range(5, 21),
        'long_ema_period': range(20, 51),
        'rsi_period': range(10, 31)
    }

    def init(self):
        # Initialize the EMAs and RSI
        self.short_ema = self.I(EMA, self.data.Close, self.short_ema_period)
        self.long_ema = self.I(EMA, self.data.Close, self.long_ema_period)
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)

    def next(self):
        # Buy condition: short EMA crosses above long EMA and RSI < 30
        if crossover(self.short_ema, self.long_ema) or self.rsi[-1] < 30:
            self.buy()

        # Sell condition: short EMA crosses below long EMA and RSI > 70
        elif crossover(self.long_ema, self.short_ema) or self.rsi[-1] > 70:
            self.sell()


class SmaCross(Strategy):
    def init(self):
        # Define two simple moving averages (SMA)
        self.sma1 = self.I(SMA, self.data.Close, 10)
        self.sma2 = self.I(SMA, self.data.Close, 20)

    def next(self):
        # Buy signal: sma1 crosses above sma2
        if crossover(self.sma1, self.sma2):
            self.buy()
        # Sell signal: sma1 crosses below sma2
        elif crossover(self.sma2, self.sma1):
            self.sell()

# Perform the backtest
bt = Backtest(df_last_10000, EMARsiStrategy, cash=10_000, commission=.002)
parameter_grids = {
    'short_ema_period': range(5, 75, 5),  # Example range for short EMA period
    'long_ema_period': range(20, 500, 5),  # Example range for long EMA period
    'rsi_period': range(10, 500, 5)        # Example range for RSI period
}

best = bt.optimize(**parameter_grids)
#output = bt.run()
#print(output)
print(best['_strategy'])
#best.plot()
