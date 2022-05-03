from requests import Request, Session
import json
import os
import datetime
import time
from config import *



SLEEP_TIME = 0.2 
# URL = 'https://api2.lunarcrush.com/v2?data=market&type=fast'
# HOW_MANY_COINS = 100
# GROUP_SIZE = 400

# EXCHANGES = ['BINANCE', 'KUCOIN']
# CURRENCIES = ['USDT', 'BTC']



# ====== Setup date and time ===========
# Date
generation_date = datetime.datetime.now()
generation_date = generation_date.strftime("%d_%m_%y")


# Time now
t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
#print(current_time)


#generation_time = now.strftime("%H:%M:%S")


#=============================================

# ======== Step 0 ==========
# http requests
# return any array of dictionaries

url = URL

headers = {
    'Accepts': 'application/json'
}

parameters = {
    'limit': HOW_MANY_COINS
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
#print(response.json()["data"][1]["s"])
#print(response.json()["data"])
parsed_response = response.json()["data"]

#================================================ # 
# Step 1 #
# Turn Json response to a list of symbols
# [ 'BTC', "ETH", ...] 
# store in symbols

symbols = []
def json_to_tickers(data):
    for item in data:
        symbols.append(item["s"])

json_to_tickers(parsed_response)
#print(symbols)

# now symbols hold all our ..well.. symbols

#================================================ # 
# Step 2 # 
# Helper Function
# Convert one symbol to tradingview format with exchange currency pair, in a list
# input: 'ADA'
# output: ["BINANCE:ADABTC", "BINANCE:ADAUSDT", ...]

exchanges = EXCHANGES
currencies = CURRENCIES

def symbol_to_tradingview(symbol):
    one_symbol_watchlist = []
    for exchange in exchanges:
        for currency in currencies:
            current_pair = ""
            one_symbol_watchlist.append(f"{exchange}:{symbol}{currency}")
    return one_symbol_watchlist

#symbol_to_tradingview('ADA')


#================================================
# Step 3 #
# Convert Step 1 output, which is symbols, 
#  to a list of trading view pair
# using helper from Step 2

# Flatten helper function
def flatten(t):
    return [item for sublist in t for item in sublist]

nested_tradingview_pairs=[]

for symbol in symbols:
    nested_tradingview_pairs.append(symbol_to_tradingview(symbol))

tradingview_pairs = flatten(nested_tradingview_pairs)
#print(tradingview_pairs)


#================================================
# Step 4 #
# Group output from step 3
# to a list containing lists of n 

# Group size, in production n=1000
n=GROUP_SIZE

def group_into_n(data_list, n):
    return [data_list[i:i+n] for i in range(0, len(data_list), n)]

#test = [1,2,3,4,5,6,7,8]
#print(group_into_n(test, n))

grouped_pairs = group_into_n(tradingview_pairs, n)

#print(grouped_pairs)

#================================================
# Step 5 #

# write a function to output each of the group in step 4 
# to a separate file


#def output_to_text_file(nested_grouped_pairs):
#    for idx, group in enumerate(nested_grouped_pairs):
#        with open(f'{idx+1}CMC p.{idx+1} {generation_date}.txt ', 'w') as f:
#            for pair in group:
#                f.write("%s,\n" % pair)


# /Users/raysonkong/code/python/webscrapping/scripts_v2/cmc_api_to_tradingview/outputs
def output_to_text_file(nested_grouped_pairs):
    for idx, group in enumerate(nested_grouped_pairs):
            filename=f"{os.getcwd()}/LC_{generation_date}total{HOW_MANY_COINS}/{idx+1}.LC p.{idx+1} ({generation_date}).txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                for pair in group:
                  f.write("%s,\n" % pair)



def run_srapper():
    os.system('clear')
    print("================ Getting Data =======================")
    print("\n")
    output_to_text_file(grouped_pairs)

    time.sleep(SLEEP_TIME)
    print("Requesting Data from LunarCrush...")
    time.sleep(SLEEP_TIME)
    print("...")
    time.sleep(SLEEP_TIME)
    print("Parsing Data...")
    print("...")
    time.sleep(SLEEP_TIME)
    print("Outputting Data to files...")
    time.sleep(SLEEP_TIME)
    print("....")
    print("Latest Symbol Files are created Successfully!")
    print("\n")

    print("================= Scrapping Completed ================")

if __name__ =='__main__':
    run_srapper()

