
# coding: utf-8

# In[1]:


import requests
import time
import datetime
from binance.client import Client
client = Client("FYBPA3hwLDXC5C9UIIPumTmOBmh89Mw4HCrubcyUepeqhOYyXyzKtlYoJiNdlhZQ", "TLG8kauzBuA7wm1UDsU3sS0mYdO4z0IB36Seqb1OgJQpyOznREqILUCssRIslFgD")
f_name = "binance-data_15min.csv"
f = open(f_name,"a")
keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
vals = [0]*len(keys)



while True:

    data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()[0]
    # bstamp = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json() 
    # bkc = requests.get("https://blockchain.info/ticker").json()

    temp_data = client.get_klines(
        symbol="BTCUSDT",
        interval=Client.KLINE_INTERVAL_15MINUTE,
        limit=500
    )
    binance_last = temp_data[len(temp_data) - 1]
    price = binance_last[4]
    volume = float(binance_last[5]) * float(price)
    n_trades = binance_last[8]

    for d in data.keys():
        if d in keys:
            if d == "market_cap_usd": 
                market_cap = data[d]
            if d == "available_supply":
                available_supply = data[d]

    f.write("{},{},{},{},{}".format(price, volume, n_trades, market_cap, available_supply))
    # #f.write("{},{},".format(bstamp["volume"],bstamp["vwap"]))
    # f.write("{},{},{}".format(bkc["USD"]["sell"],bkc["USD"]["buy"],bkc["USD"]["15m"]))
    f.write(","+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
    f.write("\n")
    f.flush()
    time.sleep(900)
