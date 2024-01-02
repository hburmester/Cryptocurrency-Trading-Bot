import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import os

# Replace these with your API keys
api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')

# Initialize the exchange (replace 'binance' with your preferred exchange)
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key,
})

# Define the trading pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1d'  # Daily timeframe

# Fetch historical OHLCV (Open/High/Low/Close/Volume) data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Function to identify and plot breakout trades
def breakout_strategy(data, support_window=30, resistance_window=30):
    # Calculate support and resistance levels
    data['support'] = data['low'].rolling(window=support_window).min()
    data['resistance'] = data['high'].rolling(window=resistance_window).max()

    # Identify breakout signals
    data['long_signal'] = (data['close'] > data['resistance']) & (data['close'].shift(1) <= data['resistance'].shift(1))
    data['short_signal'] = (data['close'] < data['support']) & (data['close'].shift(1) >= data['support'].shift(1))

    # Plot breakout signals
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['close'], label='Close Price', linewidth=2)
    plt.plot(data['timestamp'], data['resistance'], label='Resistance', linestyle='--', color='green')
    plt.plot(data['timestamp'], data['support'], label='Support', linestyle='--', color='red')

    # Plot long signals
    plt.plot(data[data['long_signal']]['timestamp'], data[data['long_signal']]['close'], '^', markersize=10, color='g', label='Buy Signal')

    # Plot short signals
    plt.plot(data[data['short_signal']]['timestamp'], data[data['short_signal']]['close'], 'v', markersize=10, color='r', label='Sell Signal')

    plt.title('Breakout Trading Strategy')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Apply breakout strategy to the data
breakout_strategy(df)
