import sys # mainly for command line args
import requests # http requests
import json # for parsing data

if len(sys.argv) != 3:
	print('Usage: python3 stocks.py <stock symbol> <ifttt webohoks key>')
	exit()

# I'm using bloomberg's api to get stock information
STOCK_API = 'https://www.bloomberg.com/markets2/api/datastrip/{0}?locale=en'
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

percent = json_data[0]['percentChange1Day']
date = json_data[0]['tradingDayClose'].split('T')[0]

# send the data to IFTTT webhooks
response = requests.get(IFTTT_WEBHOOK_API.format(webhook_key, stock, date, percent))

# print a summary
print('STOCK: {}'.format(stock))
print('{0} - Changed {1}%'.format(date, round(percent, 2)))
print('Data sent to IFTTT with response: {}'.format(response.text))
