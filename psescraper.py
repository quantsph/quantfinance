#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:31:10 2017

@author: lampil
"""



def get_stock_data(symbol, start_date, end_date):

    # import modules
    import requests
    import pandas as pd
    import time
    import datetime
    import dateutil.parser

    # convert date range to POSIX timestamp
    start_timestamp = time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple())    
    end_timestamp = time.mktime(datetime.datetime.strptime(end_date, "%Y-%m-%d").timetuple())   
#    start_timestamp = int(dateutil.parser.parse(start_date).timestamp())
#    end_timestamp = int(dateutil.parser.parse(end_date).timestamp())

    # define the api-endpoint 
    api_endpoint = "https://www.investagrams.com/InvestaApi/TradingViewChart/history?symbol=" + \
                    symbol + "&resolution=D&from=" + \
                    str(start_timestamp) + "&to=" + str(end_timestamp)

    # send post request and save response as response object
    r = requests.post(url = api_endpoint, data = {})

    prices_df = (pd.DataFrame({'Timestamp':r.json()['t'], 
                               'Open':r.json()['o'], 
                               'High':r.json()['h'],
                               'Low':r.json()['l'],
                               'Close':r.json()['c'],
                               'Volume':r.json()['v'],
                              })
                 .assign(Date = lambda x: x['Timestamp'].apply(datetime.datetime.fromtimestamp).values.astype('<M8[D]'))
                 .drop('Timestamp', axis=1)
                 .set_index('Date')
                 .loc[:,['Open','High','Low','Close','Volume']]
                )
    
    return prices_df

import pygsheets
import datetime as dt

tickers = ['ALI','FGEN','EDC','JFC','MEG']
start_date = '2017-01-01'
end_date = '2017-02-01'

contract_url = 'https://docs.google.com/spreadsheets/d/1AUjmRVZ1DlVXx1P8yKA6QOZSN3m-9RP8FXk3sfesZ3Q/edit#gid=0'
tab_name = 'master'

gc = pygsheets.authorize(service_file='/Users/lampil/Documents/Automations/LiveOpsAutomation/service_key.json')
pse_sh = gc.open_by_url(contract_url).worksheet('title',tab_name)
stock_vals_all = pse_sh.get_all_values()
stock_list = list(enumerate([str(stock[1]) for stock in stock_vals_all][1:]))

for ticker in stock_list[225:]:
    ticker = ticker[1]
    try:
        print "Currently running {} ...".format(ticker)
        df = get_stock_data(ticker, "2012-01-01", "2017-09-27")
        df['Date'] = df.index
        df['Date'] = df['Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
        print "Query for {} Successful!".format(ticker)
        gc = pygsheets.authorize(service_file='/Users/lampil/Documents/Automations/LiveOpsAutomation/service_key.json')
        gc.open_by_url(contract_url).add_worksheet(ticker, rows=5000, cols=7, src_tuple=None, src_worksheet=None)
        pse_sh_ws = gc.open_by_url(contract_url).worksheet('title',ticker)
        pse_sh_ws.update_cells(crange="A1", values = [list(df.columns)] + df.values.tolist())
        print "Pasting for {} Successful!".format(ticker)
    except:
        print "An error occurred for {}. Skipping ...".format(ticker)
        continue







