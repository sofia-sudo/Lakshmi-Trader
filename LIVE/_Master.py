import pandas as pd
import time

## Initialise all modules of the software
import PortfolioEngine
import TradeEngine
import ExchangeEngine
import CLI

## Control constants; will define the running parameters of the program
## Determine the assets to be managed and indicators calculated here
STK_TOKENS  = ['SPY', 'GLD']
CPT_TOKENS  = ['BTC/USD', 'ETH/USD']
INDICATORS  = ['EMA', 'RSI', 'BB']
TICK_LENGTH = 60

##### TEST VALUES ######
### Used to isolate parts of the program by creating a standardised testing environment
### with predictable expected behaviour.
## STK_TOKENS -> SPY and GLD
## CPT_TOKENS -> BTC/USD and ETH/USD
## INDICATORS -> EMA, RSI and BB
## TICK_LENGTH -> 20        # Faster than in operation to speed up cycles for testing
###// TEST VALUES //####


## Initialises the software by subscribing relevant traders, assets and indicators
def Initialise():
    # Subscribe Stock tokens to the software
    for token in STK_TOKENS:
        TradeEngine.SubscribeStkTrader(token)
        ExchangeEngine.SubscribeStkAsset(token)
    
    # Subscribe Crypto tokens to the software
    for token in CPT_TOKENS:
        TradeEngine.SubscribeCptTrader(token)
        ExchangeEngine.SubscribeCptAsset(token)
    
    # Subscribe indicators
    for indicator in INDICATORS:
        ExchangeEngine.SubscribeIndicator(indicator)

    # Initialise modules in order
    PortfolioEngine.UpdatePositions()
    ExchangeEngine.Initialise() # Cascades to initialise MarketEngine, HistoricalDataEngine

## The core cycle for the software to operate perpetually
def Cycle():
    iteration_counter = 0
    last_tick_time = 0
    while True:
        iteration_counter += 1
        t = time.time()

        # Reset UI for next tick
        CLI.Home(iteration_counter, last_tick_time)

        # Check current portfolio status
        CLI.SectionHeader('SYSTEM', 'Open Positions')
        PortfolioEngine.UpdatePositions()
        

        # Pull latest data from market & process indicators
        CLI.SectionHeader('SYSTEM', 'Exchange Information')
        ExchangeEngine.Update()

        # Execute strategy, make appropriate orders and close appropriate positions
        TradeEngine.Update()

        # Pause to not overload API
        last_tick_time = time.time() - 2
        CLI.Delay(max(TICK_LENGTH - (time.time() - t), TICK_LENGTH/2))

## Start the software
Initialise()
Cycle()
