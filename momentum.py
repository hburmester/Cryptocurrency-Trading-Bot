import ccxt
import pandas as pd
import talib
import time

# Replace these with your API keys
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_API_SECRET'

# Initialize the exchange (replace 'binance' with your preferred exchange)
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key,
})

# Define the trading pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'  # 1-hour timeframe

# Function to fetch historical OHLCV data
def fetch_historical_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Function to implement momentum trading strategy
def momentum_trading_strategy(data, rsi_period=14, rsi_overbought=70, rsi_oversold=30, stop_loss_percentage=1):
    # Calculate RSI
    data['rsi'] = talib.RSI(data['close'], timeperiod=rsi_period)

    # Identify overbought and oversold conditions
    data['overbought'] = data['rsi'] > rsi_overbought
    data['oversold'] = data['rsi'] < rsi_oversold

    # Initialize position column (-1 for short, 1 for long, 0 for no position)
    data['position'] = 0

    # Enter long position when oversold condition and rising RSI
    data.loc[(data['oversold']) & (data['rsi'].shift(1) < data['rsi']), 'position'] = 1

    # Enter short position when overbought condition and falling RSI
    data.loc[(data['overbought']) & (data['rsi'].shift(1) > data['rsi']), 'position'] = -1

    # Set stop-loss orders
    data['stop_loss'] = data['close'] * (1 - stop_loss_percentage / 100)

    # Execute trades based on position changes
    data['signal'] = data['position'].diff()

    return data

# Apply momentum trading strategy to the data
historical_data = fetch_historical_data(symbol, timeframe)
strategy_results = momentum_trading_strategy(historical_data)

# Print the resulting DataFrame with trading signals and RSI
print(strategy_results[['timestamp', 'close', 'rsi', 'position', 'stop_loss', 'signal']])
