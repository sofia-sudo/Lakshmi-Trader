## Imports
import pandas as pd
import concurrent.futures
import threading

from concurrent.futures import ThreadPoolExecutor

import MarketEngine
import DataEngine
import CLI

## Config
memory_limit = 30000 # Limit on records
stk_tokens   = [] # Subscribed stock assets
cpt_tokens   = [] # Subscribed crypto assets
indicators   = [] # Subscribed indicators
exchange     = {} # Dictionary of Dataframes

## Drops older records on the exchange to stay within memory limits.
def EnforceExchangeMemoryLimits(token):
    exchange[token] = exchange[token].reset_index()
    exchange[token] = exchange[token].iloc[-memory_limit:]

## Retrieves historical data and registers a given asset to the exchange
def RegisterStkAssetToExchange(token):
    exchange[token] = MarketEngine.GetStkHistoricalData(token)
    EnforceExchangeMemoryLimits(token)

## Retrieves historical data and registers a given asset to the exchange
def RegisterCptAssetToExchange(token):
    exchange[token] = MarketEngine.GetCptHistoricalData(token)
    EnforceExchangeMemoryLimits(token)

## Initialises the ExchangeEngine
## - Establishes asset-level memory limits
## - Subscribes each token to the MarketEngine
## - Cascade: initialises the MarketEngine
## - Registers each asset to the exchange
def Initialise():
    global memory_limit
    memory_limit = round(memory_limit / (len(stk_tokens) + len(cpt_tokens)))

    # Subscribe MarketEngine
    for token in stk_tokens:
        MarketEngine.SubscribeStkToken(token)
    
    for token in cpt_tokens:
        MarketEngine.SubscribeCptToken(token)

    # Intialise MarketEngine
    MarketEngine.Initialise()

    # Populate historical data
    pool = ThreadPoolExecutor(max_workers=6)

    for stk_token in stk_tokens:
        pool.submit(RegisterStkAssetToExchange(stk_token))
    
    for cpt_token in cpt_tokens:
        pool.submit(RegisterCptAssetToExchange(cpt_token))
        
    pool.shutdown(wait=True)

## Updates a specific asset, given the latest quote
def UpdateExchangeAsset(token, latest_quotes):
    exchange[token] = pd.concat([exchange[token], pd.DataFrame([latest_quotes])], ignore_index=True)

## Subscribes to a given indicator
def SubscribeIndicator(indicator):
    global indicators
    indicators.append(indicator)

## Subscribes to a given stock asset
def SubscribeStkAsset(token):
    global stk_tokens
    stk_tokens.append(token)

## Subscribes to a given crypto asset
def SubscribeCptAsset(token):
    global cpt_tokens
    cpt_tokens.append(token)

## Tick Update Function
## - Retrieves latest quotes from MarketEngine
## - Updates all assets on the exchange with the new quotes
## - Processes all indicators
def Update():
    latest_quotes = MarketEngine.Update()

    for token in latest_quotes:
        UpdateExchangeAsset(token, latest_quotes[token])        
    
    # Calculate all indicators
    ProcessAllIndicators()

    # UI update
    try:
        # Calculate memory usage
        memory_usage = 0

        for token in exchange.keys():
            memory_usage += len(exchange[token])
            CLI.OutputTokenTicker(token, exchange[token])

        # Display memory usage
        CLI.Log('EXCHANGE', f'Memory Usage: {memory_usage}/{memory_limit * (len(stk_tokens) + len(cpt_tokens))}')

    # Do not break on this error; it is non-critical, but may imply an underlying problem.
    except: 
        CLI.Log('EXCHANGE', 'Non-Critical Error in UI rendering. Check memory limits and Exchange.exchange integrity.')
        return
    
    

## Processes the data for each indicator subscribed.
def ProcessAllIndicators():
    for indicator in indicators:
        for token in stk_tokens + cpt_tokens:
            exchange[token] = DataEngine.ExecuteIndicatorFromString(exchange[token], indicator)

