import datetime
#
import pandas as pd
from pandas_datareader import test
import matplotlib.pyplot as plt
import numpy as np
#
import yfinance as yf
import quandl
#
import enum

from model import *

def show_values(portfolio: Portfolio):
    stocks = portfolio.get_stock_list()
    for stock in stocks:
        df_yahoo = yf.download(['CRM'   , 'DDD', 'PRLB'],
                       start='2018-01-01',
                       end='2022-1-28',
                       # auto_adjust=True,
                       progress=False)
        
#
# load portfolio
#
portfolio = load_portfolio('portfolio.json')
portfolio.show_accounts()



# 
# Quandl : keys
#
QUANDL_KEY = "zSQgVZXfyBf_ek_efub5"
quandl.ApiConfig.api_key = QUANDL_KEY
#
df_yahoo = yf.download(['CRM'   , 'DDD', 'PRLB'],
                       start='2018-01-01',
                       end='2022-1-28',
                       # auto_adjust=True,
                       progress=False)

df = df_yahoo.loc[:, ['Adj Close']]
df.rename(columns={'Adj Close': 'adj_close'}, inplace=True)

# Download inflation data from Quandl
dates = pd.date_range(
    start='2018-01-01',
    end='2022-01-28'
)

# Download inflation data from Quandl
df_cpi = quandl.get(dataset='RATEINF/CPI_FRA', 
                    start_date='2018-01-01', 
                    end_date='2022-1-28')
df_cpi.rename(columns={'Value':'cpi'}, inplace=True)
# Create a DataFrame with all possible dates and left join the prices on it
df_all_dates = pd.DataFrame(index=pd.date_range(start='2018-01-01',
                                                end='2022-01-28'))
df = df_all_dates.join(df[['adj_close']], how='left') \
                 .fillna(method='ffill') \
                 .asfreq('M')
# Merge inflation data to prices:              
df_merged = df.join(df_cpi, how='left')
# Calculate simple returns and inflation rate
df_merged['simple_rtn'] = df_merged.adj_close.pct_change()
df_merged['inflation_rate'] = df_merged.cpi.pct_change()
# Adjust returns for inflation
df_merged['real_rtn'] = (df_merged.simple_rtn + 1) / (df_merged.inflation_rate + 1) - 1
df_merged.head()

# result = pd.read_sql(text('SELECT name FROM students'), conn)
# print(result)
# #with engine.connect() as conn:
# #    result = conn.execute(ins)
# #    for item in result.cursor():
# #        print(type(item))
