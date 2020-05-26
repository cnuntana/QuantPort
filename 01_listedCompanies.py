# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:06:49 2020

@author: Dew
"""


import pandas as pd
import yfinance as yf
import yahoofinancials
from datetime import date, timedelta
import matplotlib.pyplot as plt
import os 
import urllib.request

import warnings
warnings.filterwarnings("ignore")

os.chdir(r"C:\Users\Dew\Git Projects\QuantPort") 
df = pd.read_csv('listedCompanies.csv',encoding='utf-8')

df['Market Cap'] = 'nan'
for i in range(len(df)):
    try:
        name = df['Symbol'].iloc[i]
        url='https://www.set.or.th/set/companyprofile.do?symbol='+name+'&ssoPageId=4&language=en&country=US'
        page = urllib.request.urlopen(url)
        aaa =str(page.read())
        start = aaa.find('Market Cap')
        start = aaa.find('<div class="col-xs-9 col-md-5">',start)+31
        end = aaa.find('.', start)+3
        if '</div>\\n' in aaa[start:end]:
            df['Market Cap'].iloc[i] = 0
        else:
            df['Market Cap'].iloc[i]=aaa[start:end]
        print(i)
    except:
        print(df['Symbol'].iloc[i])

for i in range(len(df)):
    if df['Market Cap'].iloc[i]=='nan':
        try:
            name = df['Symbol'].iloc[i]
            url='https://www.set.or.th/set/companyprofile.do?symbol='+name+'&ssoPageId=4&language=en&country=US'
            page = urllib.request.urlopen(url)
            aaa =str(page.read())
            start = aaa.find('Market Cap')
            start = aaa.find('<div class="col-xs-9 col-md-5">',start)+31
            end = aaa.find('.', start)+3
            if '</div>\\n' in aaa[start:end]:
                df['Market Cap'].iloc[i] = 0
            else:
                df['Market Cap'].iloc[i]=aaa[start:end]
            print(i)
        except:
            print(df['Symbol'].iloc[i])
            
df2=df.drop( df[ df['Symbol'] == 'S & J' ].index)

for i in range(len(df2)):
    try:
        float(df2['Market Cap'][i])
    except:
        df2=df2.drop([i])
        
df2=df.drop( df[ df['Symbol'] == 'S & J' ].index)
df2['Market Cap']=df2['Market Cap'].str.replace(',','')
df2['Market Cap']=df2['Market Cap'].fillna(0).astype(float)

df2[df2['Market Cap']>10000].to_csv('stock_with_MC.csv')















