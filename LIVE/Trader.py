## Imports
import pandas as pd
import DataEngine
import requests
import CONFIG
import CLI


## Manages the trading for 1 asset
class Trader:
    def __init__(self, _token, _position_open=False):
        self.token         = _token # Token to manage
        self.position_open = _position_open # Boolean: is a position open? default=False
    
    ## Places a new market order
    ## API REFERENCE: [https://docs.alpaca.markets/reference/postorder]
    def NewMarketOrder(self, qty, notional=True, side='buy', time_in_force='day', force_order=False):
        if self.position_open and not force_order:
            CLI.Log(f'TRADER${self.token}', 'Tried to place order but position is already open. Set force_order to True to place anyway.')
            return False

        url = "https://paper-api.alpaca.markets/v2/orders"

        # Construct payload
        payload = {
            "side": side,
            "type": "market",
            "time_in_force": time_in_force,
            "symbol": self.token
        }

        # Construct headers
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "APCA-API-KEY-ID": CONFIG.API_KEY,
            "APCA-API-SECRET-KEY": CONFIG.API_SECRET
        }

        # Add amount
        if notional:
            payload['notional'] = qty
        else:
            payload['qty'] = qty

        # Execute
        response = requests.post(url, json=payload, headers=headers)

        # Log to UI
        CLI.Log(f'TRADER${self.token}', f'Opened a position for {qty}')

        return response

    ## Closes an open position by a given percent (default 100%)
    ## API REFERENCE: [https://docs.alpaca.markets/reference/deleteopenposition-1]
    def ClosePosition(self, percentage_to_close=100):
        # Check if position is open
        if self.position_open:

            # Convert symbol to interface with positions API
            if '/' in self.token:
                symbol = self.token.replace('/', '')
            else:
                symbol = self.token
            
            # Construct URL
            url = f"https://paper-api.alpaca.markets/v2/positions/{symbol}?percentage={percentage_to_close}"

            # Construct headers
            headers = {
                "accept": "application/json",
                "APCA-API-KEY-ID": CONFIG.API_KEY,
                "APCA-API-SECRET-KEY": CONFIG.API_SECRET
            }

            # Execute
            response = requests.delete(url, headers=headers)

            self.position_open = False

            # Log to UI
            CLI.Log(f'TRADER${self.token}', f'Closed a position for {percentage_to_close}%')

            return response

    ## Checks if any positions are eligible to be closed (1% profit)
    def CheckCloseConditions(self, position):
        if float(position['unrealized_plpc']) >= 1:
            # Log to UI
            CLI.Log(f'TRADER${self.token}', f'Closing a position for {position["unrealized_plpc"]}% Profit')

            # Close position
            self.ClosePosition(100)
            return True
        else:
            return False