## Imports
import pandas as pd

import ExchangeEngine
import PortfolioEngine
import Trader

# Config
traders  = []
strategy = ''

## Subscribes a Stock Trader to the TradeEngine
def SubscribeStkTrader(token):
    global traders
    trader = Trader.Trader(token, PortfolioEngine.CheckForOpenPosition(token))
    traders.append(trader)

## Subscribes a Crypto Trader to the Trade Engine
def SubscribeCptTrader(token):
    global traders
    trader = Trader.Trader(token, PortfolioEngine.CheckForOpenPosition(token))
    traders.append(trader)

# Executes strategy / Calculates Flags for a given token and dataset
def ExecuteStrategy(data):
    if len(data) == 0:
        raise ValueError('Data is Null or Empty')

    ### STRATEGY ###
    ## NOTE: Placeholder; will move to separate class 'StrategyEngine' in future version
    ## StrategyEngine will allow custom strategies for different classes.
    ## StrategyEngine will also adjust strategies on the fly to reflect market conditions
    latest_quote = data.iloc[-1]

    rsi_condition = latest_quote['RSI'] <= 30
    ema_condition = latest_quote['EMA SHORT'] >= latest_quote['EMA LONG']
    bband_condition = latest_quote['ASK PRICE'] <= latest_quote['LOW B.BAND']

    if (rsi_condition and ema_condition) or (rsi_condition and bband_condition):
        return 1
    else:
        return 0

## Executes the output of a flag; Buys on a BUY signal, sells on a SELL signal[NOT IMPLEMENTED]
def ExecuteStrategyOutput(trader, flag):
    if flag >= 1: # BUY - NOTE: flag will change to Float to indicate order priority & expected PL, will affect qty traded
        trader.NewMarketOrder(100*flag)
        
## Iteratively calls CheckCloseConditions() on all Traders. Closes if criteria met.
def CheckAllCloseConditions():
    for trader in traders:

        # Check if this trader has an open position
        if trader.token in PortfolioEngine.positions.keys():

            # Check close conditions; returns 1 if a position is closed
            sale = trader.CheckCloseConditions(PortfolioEngine.positions[trader.token])

            # If a position is closed, update this on the PortfolioEngine
            if sale == 1:
                PortfolioEngine.ClosePosition(trader.token)

## Update function for the TradeEngine; executes 1 tick
## - Executes strategy on all traders
## - Executes strategy output
## - Checks close conditions for all traded open positions
def Update():
    for trader in traders:
        ExecuteStrategyOutput(trader, ExecuteStrategy(ExchangeEngine.exchange[trader.token]))
        
    # Check sale conditions
    CheckAllCloseConditions()
