from binance.client import Client
import os

api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')

# Initialize the Binance client
client = Client(api_key, secret_key)

# Replace with the trading pair and quantity you want to trade
symbol = 'POWRUSDT'
quantity = 10  # Adjust the quantity based on your requirements

def execute_market_order(symbol, quantity):
    try:
        # Place a market order to buy (you can use create_order for more advanced order types)
        order = client.create_test_order(
            symbol=symbol,
            side='SELL',  # 'BUY' for buying, 'SELL' for selling
            type='MARKET',
            quantity=quantity
        )

        # Print the order details
        print("Order ID:", order['orderId'])
        print("Symbol:", order['symbol'])
        print("Type:", order['type'])
        print("Side:", order['side'])
        print("Quantity:", order['origQty'])
        print("Price:", order['price'])
        print("Status:", order['status'])

    except Exception as e:
        print("Error placing order:", str(e))

if __name__ == "__main__":
    execute_market_order(symbol, quantity)
