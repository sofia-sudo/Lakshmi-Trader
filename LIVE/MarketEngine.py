## Imports
import pandas as pd
import requests
import json

import HistoricalDataEngine
import CONFIG

# ENDPOINT FOR REST API (MARKET DATA API)
stk_url          = ''
stk_base_url     = "https://data.alpaca.markets/v2/stocks/quotes/latest?"
stk_exchange_url = "&feed=iex"
stk_token_url    = 'symbols='
stk_headers      = {
    "accept":              "application/json",
    "APCA-API-KEY-ID":     CONFIG.API_KEY,
    "APCA-API-SECRET-KEY": CONFIG.API_SECRET
}

# ENDPOINT FOR REST API (CRYPTO)
cpt_url          = ''
cpt_base_url     = "https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes?"
cpt_token_url    = 'symbols='
cpt_headers      = {"accept": "application/json"}


# TOKENS LIST
stk_tokens   = []
cpt_tokens   = []

## Initialises the MarketEngine
## - Generates token URLs for retrieval of multiple tokens with 1 request
## API REFERENCE: [https://docs.alpaca.markets/reference/stocklatestquotes-1] - REFER TO URL SECTION
## API REFERENCE: [https://docs.alpaca.markets/reference/cryptolatestquotes-1] - REFER TO URL SECTION
def Initialise():
    # Get module variables
    global stk_token_url
    global stk_url
    global cpt_token_url
    global cpt_url

    # Generate token URLs
    for token in stk_tokens:
        stk_token_url += token + '%2C'
    stk_token_url = stk_token_url[:-3]

    for token in cpt_tokens:
        cpt_token_url += token + '%2C'
    cpt_token_url = cpt_token_url[:-3]

    # Generate complete URL
    stk_url = stk_base_url + stk_token_url + stk_exchange_url
    cpt_url = cpt_base_url + cpt_token_url

## Subscribes a token to monitor
def SubscribeStkToken(token):
    global stk_tokens
    stk_tokens.append(token)

## Subscribes a crypto pair to monitor
def SubscribeCptToken(token):
    global cpt_tokens
    cpt_tokens.append(token)

## Retrieve all latest quotes and return one combined dictionary
def Update():
    if len(stk_tokens) == 0:
        return CptUpdate()
    elif len(cpt_tokens) == 0:
        return StkUpdate()
    else:
        return StkUpdate() | CptUpdate()

## Retrieve and process latest quotes from Stock Market. Returns dictionary
def StkUpdate():
    if len(stk_tokens) == 0:
        return
    
    # Get latest quotes [https://docs.alpaca.markets/reference/stocklatestquotes-1]
    response = requests.get(stk_url, headers=stk_headers)

    # Convert to dictionary-py
    dict = json.loads(response.text)
    dict = dict['quotes']

    # Format dictionaries
    for token in stk_tokens:
        dict[token].pop('ax')
        dict[token].pop('bx')
        dict[token].pop('c')
        dict[token].pop('z')
        dict[token]['TIMESTAMP']  = dict[token].pop('t')
        dict[token]['ASK PRICE']  = dict[token].pop('ap')
        dict[token]['ASK SIZE']   = dict[token].pop('as')
        dict[token]['BID PRICE']  = dict[token].pop('bp')
        dict[token]['BID SIZE']   = dict[token].pop('bs')
    
    # Return dictionary
    return dict

## Retrieve and process latest quotes from Crypto. Returns dictionary
def CptUpdate():
    if stk_token_url == 'symbols=':
        return
    # Get latest quotes [https://docs.alpaca.markets/reference/cryptolatestquotes-1]
    response = requests.get(cpt_url, headers=cpt_headers)

    # Convert to dictionary-py
    dict = json.loads(response.text)
    dict = dict['quotes']

    # Format dictionaries
    for token in cpt_tokens:
        dict[token]['TIMESTAMP']  = dict[token].pop('t')
        dict[token]['ASK PRICE']  = dict[token].pop('ap')
        dict[token]['ASK SIZE']   = dict[token].pop('as')
        dict[token]['BID PRICE']  = dict[token].pop('bp')
        dict[token]['BID SIZE']   = dict[token].pop('bs')
    
    # Return dictionary
    return dict

def GetStkHistoricalData(token):
    return HistoricalDataEngine.GetStkData(token)

def GetCptHistoricalData(token):
    return HistoricalDataEngine.GetCptData(token)