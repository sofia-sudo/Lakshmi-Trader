## TODO: CONVERT FROM SDK TO RESTFUL API
## REASONING: The REST API is considerably more reliable, and considerably more readable
## This code is an absolute mess because the SDK is poorly designed
## Converting to REST would dramatically reduce the filesize, improve readability, improve reliability
##  and possibly improve performance; this code takes too long to execute.
## KNOWN ISSUE: The SDK does not support NP tokens, this is causing inefficiency in data transfer.
##  SOLUTION: Convert to REST

## Imports
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, CryptoLatestQuoteRequest
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from alpaca.data.models.bars import Bar
from alpaca.data.enums import DataFeed

import requests
import CONFIG

## Retrieves historical bars for a given stock asset
## API REFERENCE: [https://docs.alpaca.markets/reference/stockbars] - RESTful
## API REFERENCE: [https://alpaca.markets/sdks/python/market_data.html#retrieving-historical-bar-data] - SDK
def GetStkData(token):
    client = StockHistoricalDataClient(CONFIG.API_KEY, CONFIG.API_SECRET)

    # Formulate request parameters
    request_params = StockBarsRequest(
        symbol_or_symbols=token,
        timeframe=TimeFrame.Minute,
        start=datetime.now() + timedelta(hours=-72, minutes=-16),
        end=datetime.now() + timedelta(minutes=-16),
        feed=DataFeed.IEX
    )

    # Retrieve bars
    bars = client.get_stock_bars(request_params)

    # Construct dataframe
    df = pd.DataFrame()

    # Convert bars into pd.DataFrame
    for i in range(0, len(bars[token])):
        record = {
            'TIMESTAMP' : bars[token][i].timestamp,
            'ASK PRICE' : bars[token][i].close,
            'BID PRICE' : bars[token][i].close
        }

        dfRecord = pd.DataFrame([record])
        df = pd.concat([df, dfRecord], ignore_index=True)
    
    # Return dataframe
    return df

## Retrieves historical bars for a given crypto asset
## API REFERENCE: [https://docs.alpaca.markets/reference/cryptobars-1] - RESTful
## API REFERENCE: [https://alpaca.markets/sdks/python/market_data.html#retrieving-historical-bar-data] - SDK
def GetCptData(token):
    client = CryptoHistoricalDataClient()

    # Construct request parameters
    request_params = CryptoBarsRequest(
        symbol_or_symbols=token,
        timeframe=TimeFrame.Minute,
        start=datetime.now() + timedelta(hours=-12),
        end=datetime.now()
    )

    # Get bars
    bars = client.get_crypto_bars(request_params)

    # Construct dataframe
    df = pd.DataFrame()

    # Convert bars to pd.DataFrame
    for i in range(0, len(bars[token])):
        record = {
            'TIMESTAMP' : bars[token][i].timestamp,
            'ASK PRICE' : bars[token][i].close,
            'BID PRICE' : bars[token][i].close
        }

        dfRecord = pd.DataFrame([record])
        df = pd.concat([df, dfRecord], ignore_index=True)
    
    # Return dataframe  
    return df
