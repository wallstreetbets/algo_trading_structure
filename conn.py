import pandas as pd
from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime

PUBLIC_API_KEY = ''
PRIVATE_API_KEY = ''

client = Client(PUBLIC_API_KEY, PRIVATE_API_KEY)

bm = BinanceSocketManager(client)


def engine():
    symbol = "BTCUSDT"

    client = Client(PUBLIC_API_KEY, PRIVATE_API_KEY)
    data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "{} day ago UTC".format(800))
    dates = []

    # Curate KLINE data, fix Datetime and delete useless cols
    for i in data:
        timestamp = i[0] / 1000
        timestamp = datetime.fromtimestamp(timestamp).strftime('%D')
        dates.append(timestamp)
        del i[0]
        del i[-1]
        del i[-1]
        del i[-1]
        del i[-1]
        del i[-1]
        del i[-1]

    # Create the data frame
    df = pd.DataFrame(data, index=dates, columns=["Open", "High", 'Low', 'Close', 'Volume'])
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Volume'] = pd.to_numeric(df['Volume'])

    return df


if __name__ == '__main__':
    df = engine()
    print(df)
