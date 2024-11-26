## Imports
import pandas as pd
import numpy as np

#### FORMAT NOTICE FOR .ExecuteIndicatorFromString() ####
## Take 'df' as first variable
## Follow with ALL OPTIONAL parameters
## Return modified dataframe


## Calculates EMA
def EMA(df, short_period=5, long_period=75):
    df['EMA SHORT'] = df['ASK PRICE'].ewm(span=short_period, adjust=False).mean()
    df['EMA LONG']  = df['ASK PRICE'].ewm(span=long_period, adjust=False).mean()
    return df

## Calculates RSI
def RSI(df, period=5):
    delta = df['ASK PRICE'].diff(1)

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    average_gain = gain.rolling(window=period, min_periods=1).mean()
    average_loss = loss.rolling(window=period, min_periods=1).mean()

    relative_strength = average_gain / average_loss

    df['RSI'] = 100 - (100 / (1 + relative_strength))

    return df

## Calculates Bollinger Bands
def BB(df, period=20):
    df['MID B.BAND'] = df['ASK PRICE'].rolling(window=period).mean()

    df['STD DEV']    = df['ASK PRICE'].rolling(window=period).std()

    df['TOP B.BAND'] = df['MID B.BAND'] + (2 * df['STD DEV'])
    df['LOW B.BAND'] = df['MID B.BAND'] - (2 * df['STD DEV'])

    return df

## NOTE: DEPRECATION NOTICE - There is a better method to do this. Will be patched out in future
## Executes an indicator on a given df
def ExecuteIndicatorFromString(df, indicator, params=None):
    if indicator == 'EMA':
        return EMA(df)
    elif indicator == 'RSI':
        return RSI(df)
    elif indicator == 'BB':
        return BB(df)
    
    raise NotImplementedError(f'The requested Indicator "{indicator}" is not in the directory.')
