import os
import pytz
import pandas as pd
from datetime import timedelta, timezone, datetime as dt
from typing import Any, Optional

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from alpaca.trading import TradingClient, GetOptionContractsRequest, AssetStatus, ContractType
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, OptionBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from dotenv import load_dotenv
load_dotenv()

TRADE_API_URL="https://paper-api.alpaca.markets"
DATA_API_URL=None
TRADE_API_WSS=None
OPTION_STREAM_DATA_WSS=None

class AlpacaClient():
    def __init__(self):
        api_key = os.environ.get("ALPACA_API_KEY")
        secret_key = os.environ.get("ALPACA_SECRET")

        self.tc = TradingClient(api_key=api_key, secret_key=secret_key, paper=True, url_override=TRADE_API_URL)
        self.shdc = StockHistoricalDataClient(api_key=api_key, secret_key=secret_key)

    def get_account_info(self):
        return self.tc.get_account()
    
    def get_current_positions(self):
        return self.tc.get_all_positions()
    
    def get_beginning_of_week(self, date: Optional[dt] = None):
        if date is None:
            date = dt.now(timezone.utc)
        # Convert to Eastern Time
        eastern = pytz.timezone("America/New_York")
        date_et = date.replace(tzinfo=pytz.utc).astimezone(eastern)

        # Calculate the beginning of the week (Monday at 8 AM ET)
        start_of_week = date_et - timedelta(days=date_et.weekday())  # Move to Monday
        start_of_week = start_of_week.replace(hour=8, minute=0, second=0, microsecond=0)  # Set to 8 AM
        print(start_of_week)

        return start_of_week
    
    def get_stock_history_bars(self, ticker)-> pd.DataFrame:
        req = StockBarsRequest(
            symbol_or_symbols=ticker,
            timeframe=TimeFrame(5, TimeFrameUnit.Minute), #5 minute
            start=self.get_beginning_of_week(),
        )
        df = self.shdc.get_stock_bars(req).df

        # calculate RSI & Bollinger Bands
        df = self.calculate_rsi(df)
        df = self.calculate_bollinger_bands(df)
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, period=14):
        # Compute price changes
        df['delta'] = df['close'].diff()

        # Separate gains and losses
        df['gain'] = df['delta'].where(df['delta'] > 0, 0)
        df['loss'] = -df['delta'].where(df['delta'] < 0, 0)

        # Compute rolling averages of gains and losses
        avg_gain = df['gain'].rolling(window=period, min_periods=1).mean()
        avg_loss = df['loss'].rolling(window=period, min_periods=1).mean()

        # Compute Relative Strength (RS)
        rs = avg_gain / avg_loss

        # Compute RSI
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def calculate_bollinger_bands(self, df: pd.DataFrame, window=10, width=2):
        if not set(['close']).issubset(df.columns):
            raise ValueError("DataFrame missing required columns")
        # Calculate the Simple Moving Average (SMA) and Standard Deviation for Bollinger Bands
        df['SMA'] = df['close'].rolling(window=window).mean()
        df['StdDev'] = df['close'].rolling(window=window).std()
        
        # Calculate the Upper and Lower Bollinger Bands
        df['Bollinger_UpperBand'] = df['SMA'] + (width * df['StdDev'])
        df['Bollinger_LowerBand'] = df['SMA'] - (width * df['StdDev'])
        return df

    def plot_candlestick_chart(self, df: pd.DataFrame):
        df = df.copy()
        req_cols = ['open', 'high', 'low', 'close', 'volume', 'Bollinger_UpperBand', 'Bollinger_LowerBand', 'RSI']
        if not set(req_cols).issubset(df.columns):
            raise ValueError(f"DataFrame must contain all of {req_cols}")

        # extract symbol and timestamps
        df.index = df.index.set_levels(pd.to_datetime(df.index.levels[1], utc=True), level=1)
        df.index = df.index.set_levels(df.index.levels[1].tz_convert(pytz.timezone('America/New_York')), level=1)
        symbol = df.index.get_level_values(0)[0]  # Get the stock symbol
        timestamps = df.index.get_level_values(1)  # Get timestamps

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.6, 0.2, 0.2])
        # ROW1: Candlestick Chart
        fig.add_trace(
            go.Candlestick(
                x=timestamps,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name="Candlestick"
            ),
            row=1, col=1
        )
        # Add the Bollinger Bands (upper and lower) as line traces
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=df['Bollinger_UpperBand'],
                line=dict(color='rgba(255, 0, 0, 0.6)', width=1),
                name='Upper Bollinger Band'
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=df['Bollinger_LowerBand'],
                # fill='tonexty',  # Fill the area between the bands
                # fillcolor='rgba(0, 0, 255, 0.1)',  # Blue shade with some transparency
                line=dict(color='rgba(0, 0, 255, 0.6)', width=1),
                name='Lower Bollinger Band'
            ),
            row=1, col=1
        )
        # Add the Moving Average (SMA) as a line trace
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=df['SMA'],
                line=dict(color='rgba(0, 255, 0, 0.6)', width=1),
                name='SMA'
            )
        )

        # Add RSI line chart (Row 2)
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=df['RSI'],
                mode='lines',
                name="RSI",
                line=dict(color='blue')
            ),
            row=2, col=1
        )
        # Add overbought (70) and oversold (30) lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # Add the volume plot (Row 3)
        fig.add_trace(
            go.Bar(
                x=timestamps,
                y=df['volume'],
                name='Volume',
                marker=dict(color='rgba(0, 128, 255, 0.6)')
            ),
            row=3, col=1
        )
        
        # Customize layout
        fig.update_layout(
            title=f"Candlestick Chart for {symbol}",
            xaxis_title="Timestamp",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            # xaxis=dict(type="category")  # Set x-axis to categorical to remove gaps
        )
        
        return fig
    
    def get_available_options(self, ticker, contract_type: Optional[str] = None):
        if ticker is None:
            return []
        contract_lookup = {
            "call": ContractType.CALL,
            "put": ContractType.PUT,
        }
        req = GetOptionContractsRequest(
            underlying_symbol=[ticker],
            root_symbol=ticker, # specify root symbol
            status=AssetStatus.ACTIVE,                           
            expiration_date=None, # specify expiration date (specified date + 1 day range)
            expiration_date_gte=None, # date object
            expiration_date_lte=None, # or string (YYYY-MM-DD)
            type=contract_lookup.get(contract_type, None),
            limit=5, #TEMP	
        )
        return self.tc.get_option_contracts(req)

if __name__ == "__main__":
    print("## Initiating...")
    client = AlpacaClient()
    spy_df = client.get_stock_history_bars(
        ticker="SPY"
    )
    fig = client.plot_candlestick_chart(spy_df)
    fig.show()

