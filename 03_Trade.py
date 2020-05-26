# -*- coding: utf-8 -*-
"""
Created on Wed May  6 07:07:47 2020

@author: Dew
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pBeta1=pd.read_csv('pBeta1.csv')
pBeta1.index = pd.to_datetime(pBeta1['Date'])
pBeta1.drop(['Date'],axis=1,inplace=True)

pRank=pd.read_csv('pRank.csv')
pRank.index = pd.to_datetime(pRank['Date'])
pRank.drop(['Date'],axis=1,inplace=True)

stock=pd.read_csv('stock.csv')
stock.index = pd.to_datetime(stock['Date'])
stock.drop(['Date'],axis=1,inplace=True)

dataStock=stock[stock.index.year<=2012]
dataRank=pRank[pRank.index.year<=2012]
dataBeta1=pBeta1[pBeta1.index.year<=2012]

dfPos=pd.DataFrame(np.nan,index=dataRank.index,columns=dataRank.columns)
dfSell=pd.DataFrame(np.nan,index=dataRank.index,columns=dataRank.columns)
dfValue=pd.DataFrame(np.nan,index=dataRank.index,columns=dataRank.columns)
dfProfit=pd.DataFrame(np.nan,index=dataRank.index,columns=dataRank.columns)
# - % Cut-Loss [1-32]% => 5binary
# - Number of top performance spreads [20,+10,330] => 5binary
# - % Daily Portfolio Allocation and Weight [1-32]% => 5binary
# - Window Size [15,+15,240] => 4binary
# - Buy at ? SD [1.6,+0.1,3.2] => 4binary
# - Sell at ? SD [0,+0.1,1.5] => 4binary

cutLoss = 0.1
topSpread = 50
portAlloc = 0.1
windSize = 100
buySD = 2
sellSD = 1

ratioAlloc = 0.8
maxAlloc = 0.9

money=pd.Series(data=np.nan,index=dataStock.index)
port=pd.Series(data=np.nan,index=dataStock.index)
reserve=pd.Series(data=np.nan,index=dataStock.index)
savPos=[]
savPrice=[]
savDate=[]

dayBefore=(dataStock.index.year==2010).sum()

money[dayBefore-1]=100
reserve[dayBefore-1]=0
port[dayBefore-1]=100

tempPos = {}
tempBeta1={}
tempPrice={}
tempResv={}

for t in range(dayBefore,len(dataStock)):
    
    #Sell old Position
    money[t]=money[t-1]
    reserve[t]=reserve[t-1]
    for p in list(tempPos):
        stockA=p.split('_')[0]
        stockB=p.split('_')[1]
        pCurrPrice=dataStock[stockA][t-windSize-1:t]+ dataStock[stockB][t-windSize-1:t]* tempBeta1.get(p)         
                    
        if tempPos.get(p)>=0 and tempPrice.get(p)>=0 and tempPrice.get(p)-pCurrPrice[-1]>=cutLoss*tempPrice.get(p):
            #SELL
            print(p,'  pos:',tempPos.get(p))
            print('   from:',tempPrice.get(p),'  to:',pCurrPrice[-1])
            print('      %:',pCurrPrice[-1]/tempPrice.get(p))
            print('   Date:',dfSell.index[t])
            print('    Box:1')
            dfSell[p][t]=pCurrPrice[-1]
            dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
            
            money[t]+=tempPos.get(p)*pCurrPrice[-1]
            reserve[t]-=tempResv.get(p)
            
            tempPos.pop(p)
            tempResv.pop(p)
            tempBeta1.pop(p)
            tempPrice.pop(p)
        elif tempPos.get(p)<=0 and tempPrice.get(p)>=0 and pCurrPrice[-1]-tempPrice.get(p)>=cutLoss*tempPrice.get(p): 
            #SELL
            print(p,'  pos:',tempPos.get(p))
            print('   from:',tempPrice.get(p),'  to:',pCurrPrice[-1])
            print('      %:',pCurrPrice[-1]/tempPrice.get(p))
            print('   Date:',dfSell.index[t])
            print('    Box:2')
            dfSell[p][t]=pCurrPrice[-1]
            dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
            
            money[t]+=tempPos.get(p)*pCurrPrice[-1]
            reserve[t]-=tempResv.get(p)
            
            tempPos.pop(p)
            tempResv.pop(p)
            tempBeta1.pop(p)
            tempPrice.pop(p)
        elif tempPos.get(p)>=0 and tempPrice.get(p)<=0 and  tempPrice.get(p)-pCurrPrice[-1]>=-cutLoss*tempPrice.get(p): 
            #SELL
            print(p,'  pos:',tempPos.get(p))
            print('   from:',tempPrice.get(p),'  to:',pCurrPrice[-1])
            print('      %:',pCurrPrice[-1]/tempPrice.get(p))
            print('   Date:',dfSell.index[t])
            print('    Box:3')
            if p =='TIP_KTC':
                plt.figure(figsize=(16, 12))
                a=pCurrPrice.rolling(100).mean()
                b=pCurrPrice.rolling(100).std().fillna(0)
                pCurrPrice.plot()
                a.plot()
                (a+2*b).plot()
                (a-2*b).plot()
                plt.savefig(p + str(t))
                
            dfSell[p][t]=pCurrPrice[-1]
            dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
            
            money[t]+=tempPos.get(p)*pCurrPrice[-1]
            reserve[t]-=tempResv.get(p)
            
            tempPos.pop(p)
            tempResv.pop(p)
            tempBeta1.pop(p)
            tempPrice.pop(p)
        elif tempPos.get(p)<=0 and tempPrice.get(p)<=0 and pCurrPrice[-1]-tempPrice.get(p)>=-cutLoss*tempPrice.get(p): 
            #SELL
            print(p,'  pos:',tempPos.get(p))
            print('   from:',tempPrice.get(p),'  to:',pCurrPrice[-1])
            print('      %:',pCurrPrice[-1]/tempPrice.get(p))
            print('   Date:',dfSell.index[t])
            print('    Box:4')
            dfSell[p][t]=pCurrPrice[-1]
            dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
            
            money[t]+=tempPos.get(p)*pCurrPrice[-1]
            reserve[t]-=tempResv.get(p)
            
            tempPos.pop(p)
            tempResv.pop(p)
            tempBeta1.pop(p)
            tempPrice.pop(p)
        else:
            meanPair = pCurrPrice[:-1].mean() 
            sdPair = pCurrPrice[:-1].std()
            if tempPos.get(p)>=0 and pCurrPrice[-1]>= meanPair-sdPair*sellSD:
                #SELL   
                dfSell[p][t]=pCurrPrice[-1]
                money[t]+=tempPos.get(p)*pCurrPrice[-1]
                dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
                
                reserve[t]-=tempResv.get(p)
                
                tempPos.pop(p)
                tempResv.pop(p)
                tempBeta1.pop(p)
                tempPrice.pop(p)
            elif tempPos.get(p)<=0 and pCurrPrice[-1]<= meanPair+sdPair*sellSD:
                #SELL
                dfSell[p][t]=pCurrPrice[-1]
                money[t]+=tempPos.get(p)*pCurrPrice[-1]
                dfProfit[p][t]= tempPos.get(p)*(pCurrPrice[-1]-tempPrice.get(p))
                
                reserve[t]-=tempResv.get(p)
                
                tempPos.pop(p)
                tempResv.pop(p)
                tempBeta1.pop(p)
                tempPrice.pop(p)
               
    #Calculate portValue
    stockValue = 0
    for p in tempPos.keys():
        stockA=p.split('_')[0]
        stockB=p.split('_')[1]
        pCurrPrice=dataStock[stockA][t]+ dataStock[stockB][t]* tempBeta1.get(p)         
        stockValue+=pCurrPrice*tempPos.get(p)
        
        dfPos[p][t]=dfPos[p][t-1]
        dfValue[p][t]=pCurrPrice
        
    port[t]=money[t]+stockValue
    
    #Check candidate Positions
    candPos={}
    candBeta1={}
    candPrice={}
    candLong={}
    candShort={}
    
    temp=dataRank.iloc[t,:]
    for p in temp[temp<=topSpread].index:
        if p not in tempPos:
            stockA=p.split('_')[0]
            stockB=p.split('_')[1]
            pCurrPrice=dataStock[stockA][t-windSize-1:t]+ dataStock[stockB][t-windSize-1:t]* dataBeta1[p][t]      
            meanPair = pCurrPrice[:-1].mean() 
            sdPair = pCurrPrice[:-1].std()
            if abs(pCurrPrice[-1])>1:
                if pCurrPrice[-1]<= meanPair-sdPair*buySD :
                    candLong[p]=dataStock[stockA]
                    candShort[p]=-dataStock[stockB]* dataBeta1[p][t]
                    
                    candPos[p]=abs(dataStock[stockA])+abs(dataStock[stockB]* dataBeta1[p][t])
                    candBeta1[p]=dataBeta1[p][t]  
                    candPrice[p]=pCurrPrice[-1]
                elif pCurrPrice[-1]>= meanPair+sdPair*buySD:
                    candLong[p]=-dataStock[stockB]* dataBeta1[p][t]
                    candShort[p]=dataStock[stockA] 
                    
                    candPos[p]=-abs(dataStock[stockA])-abs(dataStock[stockB]* dataBeta1[p][t])
                    candBeta1[p]=dataBeta1[p][t]  
                    candPrice[p]=pCurrPrice[-1]

    #Buy new Position
    if (money[t]-reserve[t])/port[t] >= 1-ratioAlloc:
        
        budget = min(portAlloc,(money[t]-reserve[t])/port[t]-1+ratioAlloc)*port[t]/len(candPrice)
        for p in candPrice.keys():
            if candPos.get(p) >0 and candPrice.get(p)>0:

                tempPos[p]=budget/candPos.get(p)
                money[t]-=tempPos[p]*candLong[p]
                reserve[t]-=tempPos[p]*candShort[p]
                
                tempBeta1[p]=candBeta1.get(p)
                tempPrice[p]=candPrice.get(p)
                
                dfPos[p][t]=tempPos.get(p)
                dfValue[p][t]=candPrice.get(p)
            elif candPos.get(p) <0 and candPrice.get(p)>0:
                money[t]+=budget
                reserve[t]+=budget
                tempPos[p]=-budget/candPrice.get(p)
                tempBeta1[p]=candBeta1.get(p)
                tempPrice[p]=candPrice.get(p)
                dfPos[p][t]=tempPos.get(p)
                dfValue[p][t]=candPrice.get(p)
            elif candPos.get(p) >0 and candPrice.get(p)<0:       
                money[t]+=budget
                reserve[t]+=budget
                tempPos[p]=-budget/candPrice.get(p)
                tempBeta1[p]=candBeta1.get(p)
                tempPrice[p]=candPrice.get(p)
                dfPos[p][t]=tempPos.get(p)
                dfValue[p][t]=candPrice.get(p)
            elif candPos.get(p) <0 and candPrice.get(p)<0:
                money[t]-=budget
                tempPos[p]=budget/candPrice.get(p)
                tempBeta1[p]=candBeta1.get(p)
                tempPrice[p]=candPrice.get(p) 
                dfPos[p][t]=tempPos.get(p)
                dfValue[p][t]=candPrice.get(p)
        savPos.append(tempPos)
        savPrice.append(tempPrice)
        savDate.append(money.index[t])
       
    
    
port.plot()

dataStock[['SPF','CPNREIT']].plot()
port.dropna().plot(figsize=(16, 12))
plt.savefig('figure')


check=dfPos.dropna(axis=1,how='all').dropna(axis=0,how='all')
check=check[check.index.year==2012]
check=check.dropna(axis=1,how='all').dropna(axis=0,how='all')

check2=dfSell[dfSell.index.year==2012]
check2=check2.dropna(axis=1,how='all').dropna(axis=0,how='all')

check3=dfValue[dfValue.index.year==2012]
check3=check3.dropna(axis=1,how='all').dropna(axis=0,how='all')

checkProfit=dfProfit[dfProfit.index.year==2012]
checkProfit=checkProfit.dropna(axis=1,how='all').dropna(axis=0,how='all')

check=dfPos.dropna(axis=1,how='all').dropna(axis=0,how='all')
money.dropna().plot(figsize=(16, 12))




dfSell['BKI_BFIT'].dropna()
dfProfit['BKI_BFIT'].dropna()
dfPos['BKI_BFIT'].dropna()
dfValue['BKI_BFIT'].dropna()



dfSell.index[t]
















