from typing import Optional
from langchain_core.tools import tool
from alpaca_trading import AlpacaClient

client = AlpacaClient()

@tool("Get Stock History Tool")
def get_stock_history_bars(ticker):
    """ Useful for retrieving stock history for a given ticker using Alpaca """
    return client.get_stock_history_bars(ticker)

@tool("Get Available Options Tool")
def get_available_options(ticker, contract_type: Optional[str] = None):
    """ Useful for retrieving available options for a given ticker using Alpaca """
    return client.get_available_options(ticker, contract_type)