import sys # mainly for command line args
import requests # http requests
import json # for parsing data

if len(sys.argv) != 3:
	print('Usage: python3 stocks.py <stock symbol> <ifttt webohoks key>')
	exit()

# I'm using bloomberg's api to get stock information
STOCK_API = 'https://www.bloomberg.com/markets/api/bulk-time-series/price/{0}?timeFrame=1_MONTH'
# IFTTT webhooks to do something useful with the info
IFTTT_WEBHOOK_API = 'https://maker.ifttt.com/trigger/stocks/with/key/{0}?value1={1}&value2={2}&value3={3}'

# command line args
stock = sys.argv[1]
webhook_key = sys.argv[2]

# get the info for the stock from the api
raw_data = requests.get(STOCK_API.format(stock))

# parse the data to json
# TODO: I should handle parsing errors here 
json_data = json.loads(raw_data.text)

# array of prices for last month
prices = json_data[0]['price']

# I'm interested in the last two prices
last_price = prices.pop()
old_price = prices.pop()

price_date = last_price['date']
old_date = old_price['date']
price_value = last_price['value']
old_value = old_price['value']

# how much it varied from previous price 
price_variance = price_value * 100 / old_value - 100

# send the data to IFTTT webhooks
response = requests.get(IFTTT_WEBHOOK_API.format(webhook_key, stock, price_date, price_variance))

# print a summary
print('STOCK: {}'.format(stock))
print('{0}: {1}'.format(old_date, round(old_value, 2)))
print('{0}: {1}'.format(price_date, round(price_value, 2)))
print('Changed {}%'.format(round(price_variance, 2)))
print('Data sent to IFTTT with response: {}'.format(response.text))
