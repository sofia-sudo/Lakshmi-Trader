## Imports
import requests
import json
import CONFIG
import CLI


positions = {} # Stores the open positions

#### NOTE: API TOKEN CONVERSION ####
## The Alpaca.Markets API and Alpaca.Positions API are inconsistent on token structure
## Alpaca.Markets, and this software, identify Crypto assets as 'CRYPTO_CURRENCY/CONVENTIONAL_CURRENCY'
## Alpaca.Positions ditches the '/' for their tokens
## This dictionary is used to convert incoming and outgoing requests at the earliest/last possible moment
## Use the second value for all use within the program, unless directly interfacing with the Positions API
compatability_conversion_table = {
    'BTCUSD' : 'BTC/USD',
    'ETHUSD' : 'ETH/USD',
    'DOGEUSD': 'DOGE/USD'
}

## Updates all positions
## - Empties positions
## - Retrieves all open positions
## - Save all positions to the positions variable
## API REFERENCE: [https://docs.alpaca.markets/reference/getallopenpositions]
def UpdatePositions():
    global positions

    # Clear positions
    positions = {}

    # Delcare URL
    url = "https://paper-api.alpaca.markets/v2/positions"

    # Construct headers
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": CONFIG.API_KEY,
        "APCA-API-SECRET-KEY": CONFIG.API_SECRET
    }

    # Execute
    response = requests.get(url, headers=headers)
    unpacked_response = json.loads(response.text)

    # Append iteratively to the positions[] list
    for position in unpacked_response:
        if position['symbol'] in compatability_conversion_table:
            positions[compatability_conversion_table[position['symbol']]] = position
        else:
            positions[position['symbol']] = position
    
    DisplayPositions()

## Displays all open positions on the console log
def DisplayPositions():
    for position in positions.values():
        CLI.Log('PORTFOLIO', f"${position['symbol']}: ${round(float(position['market_value']), 2)}@${round(float(position['avg_entry_price']), 2)} per share | Returns: {round(float(position['unrealized_plpc']), 2)}%")

## Removes a given position from the portfolio
## NOTE: This does not close the position. It simply removes it from the positions variable here
def ClosePosition(symbol):
    global positions
    positions.remove(symbol)

## Check if a given symbol has any open positions
def CheckForOpenPosition(symbol):
    if symbol in positions:
        return True
    return False
