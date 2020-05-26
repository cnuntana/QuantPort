# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:42:51 2020

@author: Dew
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 08:49:11 2020

@author: Dew
"""



import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
import os 
from datetime import date, timedelta

from statsmodels.tsa.vector_ar.vecm import VECM
from statsmodels.tsa.stattools import adfuller as adf
os.chdir(r"C:\Users\Dew\Git Projects\FinanceProj") 

listedStock = pd.read_csv('stock_with_MC.csv')
listedStock.columns
sList = listedStock['Symbol']

stock=pd.DataFrame()
df = yf.download('FUTUREPF'+'.BK', 
    start= date(2010, 1, 1),
    end = date(2020, 5, 1), 
    progress=False)
stock['TEMP']=df['Adj Close'] 

stock['TEMP'].plot()
#DOWNLOAD DATA FROM YAHOO FINANCE
for s in sList:
    df = yf.download(s+'.BK', 
        start= date(2010, 1, 1),
        end = date(2020, 5, 1), 
        progress=False)
    stock[s]=df['Adj Close']
    print(s)
    
#NAN values treatment
for s in stock.columns:
    for i in range(len(stock)-2):
        if stock[s][i+1] != stock[s][i+1]:
            if stock[s][i]==stock[s][i] and  stock[s][i+2]==stock[s][i+2]:
                stock[s][i+1]=(stock[s][i]+stock[s][i+2])/2
for s in stock.columns:
    for i in range(len(stock)-3):
        if stock[s][i+1] != stock[s][i+1] and stock[s][i+2] != stock[s][i+2]:
            if stock[s][i]==stock[s][i] and  stock[s][i+3]==stock[s][i+3]:
                stock[s][i+1]=(stock[s][i]+stock[s][i+3])/2
                stock[s][i+2]=stock[s][i+1]
for s in stock.columns:
    for i in range(len(stock)-4):
        if stock[s][i+1] != stock[s][i+1] and stock[s][i+2] != stock[s][i+2] and stock[s][i+3] != stock[s][i+3]:
            if stock[s][i]==stock[s][i] and  stock[s][i+4]==stock[s][i+4]:
                stock[s][i+1]=(stock[s][i]+stock[s][i+4])/2
                stock[s][i+2]=stock[s][i+1]
                stock[s][i+3]=stock[s][i+1]
for s in stock.columns:
    for i in range(len(stock)-5):
        if stock[s][i+1] != stock[s][i+1] and stock[s][i+2] != stock[s][i+2] and stock[s][i+3] != stock[s][i+3] and stock[s][i+4] != stock[s][i+4]:
            if stock[s][i]==stock[s][i] and  stock[s][i+5]==stock[s][i+5]:
                stock[s][i+1]=(stock[s][i]+stock[s][i+5])/2
                stock[s][i+2]=stock[s][i+1]
                stock[s][i+3]=stock[s][i+1]
                stock[s][i+4]=stock[s][i+1]
                
#check stock
for s in stock.columns:
    if stock[s].isna().sum()>500:
        print(s)

# drop some stocks which many NAN values
dropList = ['ACE','AWC','BA','BAM'
    ,'BANPU','BCPG','BGRIM','BPP'
    ,'BTSGIF','CBG','CHG','CKP'
    ,'COM7','CPTGF','CRC','DIF'
    ,'DOHOME','EA','EGATIF','EPG'
    ,'FTREIT','GPSC','GULF','GVREIT'
    ,'IMPACT','JASIF','JMT','KTIS'
    ,'M','MAJOR','MEGA','MTC'
    ,'ORI','OSP','PLANB','PRM'
    ,'PSH','PTG','SAWAD','SEG'
    ,'SPRC','TFFIF','TFG','THG'
    ,'TLGF','TOA','TPIPP','TQM'
    ,'VGI','WHA','WHART','WHAUP','SPF'
    ,'FUTUREPF','ICC','OISHI','RAM']

listedStock=listedStock.drop(listedStock[listedStock['Symbol'].isin(dropList)].index)      
stock=stock.drop(dropList,axis=1)

#check stock again
for s in stock.columns:
    if stock[s].isna().sum()>0:
        print(s)
        print(stock[s].isna().sum())

#Cluster by Industry
Industry=listedStock['Industry'].unique()


#===================================================================================
#Initial Pair Prices and ADF test
pADF=pd.DataFrame()
pHypo=pd.DataFrame()
pBeta0=pd.DataFrame()
pBeta1=pd.DataFrame()

pADF['TEMP']=stock['TEMP']
pHypo['TEMP']=stock['TEMP']
pBeta0['TEMP']=stock['TEMP']
pBeta1['TEMP']=stock['TEMP']

for ind in Industry: 
    print('Industry :', ind)
    sList = listedStock[listedStock['Industry']==ind]['Symbol']
    for i in sList:
        for j in sList:
            if i!=j and i>j:
                name= i+'_'+j
                pADF[name]=np.nan
                pHypo[name]=np.nan
                pBeta0[name]=np.nan
                pBeta1[name]=np.nan
                print(name)
                for k in range(len(stock)-244):
                    if stock[[i,j]][k:k+244].isna().sum().sum() ==0:
                        mdl = VECM(stock[[i,j]][k:k+244] ,coint_rank=1,deterministic='co')
                        res = mdl.fit()
                        x = (res.beta[0]*stock[i][k:k+244] + res.beta[1]*stock[j][k:k+244])
                        pBeta0[name][k+244]=res.beta[0]
                        pBeta1[name][k+244]=res.beta[1]
                        c = adf(x[:244],regression='c')[0]
                        pADF[name][k+244] = c
                        pHypo[name][k+244]= c<=-2.8741898504150574

pADF.drop(['TEMP'],axis=1,inplace=True)
pHypo.drop(['TEMP'],axis=1,inplace=True)
pBeta0.drop(['TEMP'],axis=1,inplace=True)
pBeta1.drop(['TEMP'],axis=1,inplace=True)
stock.drop(['TEMP'],axis=1,inplace=True)

pRank=pADF.rank(axis=1,method='min')*pHypo
pRank[pRank==0]=999

pADF.to_csv('pADF.csv')
pHypo.to_csv('pHypo.csv')
pBeta0.to_csv('pBeta0.csv')
pBeta1.to_csv('pBeta1.csv')
pRank.to_csv('pRank.csv')
stock.to_csv('stock.csv')

