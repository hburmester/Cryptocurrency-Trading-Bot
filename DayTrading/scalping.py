import ccxt
import pandas as pd
import os

api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')

# Initialize the exchange (replace 'binance' with your preferred exchange)
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key,
})

# Define the trading pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1m'

# Fetch historical OHLCV (Open/High/Low/Close/Volume) data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Simple Moving Average (SMA) indicator
def calculate_sma(data, period=30):
    return data['close'].rolling(window=period).mean()

# Bollinger Bands indicator
def calculate_bollinger_bands(data, period=30, num_std_dev=2):
    sma = calculate_sma(data, period)
    data['upper_band'] = sma + (data['close'].rolling(window=period).std() * num_std_dev)
    data['lower_band'] = sma - (data['close'].rolling(window=period).std() * num_std_dev)
    return data

# Implement scalping strategy
def scalping_strategy(data):
    data = calculate_bollinger_bands(data)
    data['signal'] = 0  # 0 for no action, 1 for buy, -1 for sell

    for i in range(1, len(data)):
        if data['close'][i] > data['upper_band'][i - 1]:
            data['signal'][i] = -1  # Sell signal
        elif data['close'][i] < data['lower_band'][i - 1]:
            data['signal'][i] = 1   # Buy signal

    return data

# Apply scalping strategy to the data
df = scalping_strategy(df)

# Print the resulting DataFrame with buy/sell signals
print(df[['timestamp', 'close', 'upper_band', 'lower_band', 'signal']])

signal_counts = df['signal'].value_counts()
print("\nSignal Counts:")
print(signal_counts)
