import pandas as pd
import formulas
from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

PUBLIC_API_KEY = 'paste public key here'
PRIVATE_API_KEY = 'paste private key here'

client = Client(PUBLIC_API_KEY, PRIVATE_API_KEY)

bm = BinanceSocketManager(client)

symbol = "BTCUSDT"

client = Client(PUBLIC_API_KEY, PRIVATE_API_KEY)
data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_6HOUR, "{} day ago UTC".format(800))
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

# Calculate formulas and add cols
df['Adj Price'] = (df['High'] + df['Low']) / 2
df['RSI'] = formulas.rsiFunc(df['Adj Price'])
df['short_Avg'] = df['Adj Price'].rolling(window=12).mean()
df['long_Avg'] = df['Adj Price'].rolling(window=26).mean()
df['BBand'] = formulas.Bolinger_Bands(df['Adj Price'], 20, 2)[0]
df['BBup'] = formulas.Bolinger_Bands(df['Adj Price'], 20, 2)[1]
df['BBlow'] = formulas.Bolinger_Bands(df['Adj Price'], 20, 2)[2]
df['DR'] = formulas.compute_daily_returns(df['Adj Price'])

# Strategy 1
df['position'] = None
for row in range(len(df)):
    if (df['RSI'].iloc[row] < 20) & (df['short_Avg'].iloc[row] < df['long_Avg'].iloc[row]) & (df['Adj Price'].iloc[row] < df['BBlow'].iloc[row]):
        df['position'].iloc[row] = -1

    if (df['RSI'].iloc[row] > 80) & (df['short_Avg'].iloc[row] > df['long_Avg'].iloc[row]) & (df['Adj Price'].iloc[row] > df['BBup'].iloc[row]):
        df['position'].iloc[row] = 1

df['position'].fillna(method='ffill', inplace=True)
df['position'].fillna(method='bfill', inplace=True)

df['Strategy Return'] = df['DR'] * df['position']

# Ploting
sub_n = 5
ax1 = plt.subplot(sub_n, 1, 1)
ax1.set_title(symbol)
df['Adj Price'].plot(label="Adj price")
plt.grid(True, linestyle='-', which='major', alpha=1)

ax2 = plt.subplot(sub_n, 1, 2, sharex=ax1)
ax2.set_title('RSI')
df['RSI'].plot()
plt.grid(True, linestyle='-', which='major', alpha=1)

ax3 = plt.subplot(sub_n, 1, 3, sharex=ax1)
ax3.set_title('Daily Returns')
df['DR'].plot()
ax1.legend()
plt.grid(True)

ax4 = plt.subplot(sub_n, 1, 4, sharex=ax1)
ax4.set_title('Volume')
df['Volume'].plot(kind='bar')

ax5 = plt.subplot(sub_n, 1, 5, sharex=ax1)
ax5.set_title('Strategy Backtest')
df['Strategy Return'].cumsum().plot()
plt.xticks(rotation=30)

plt.show()
