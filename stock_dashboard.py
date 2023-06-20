import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

st.title('Stock Market Dashboard')
st.sidebar.title('Stock Market Dashboard')
st.markdown('This application is a Streamlit dashboard for analyzing stock market picks')
st.sidebar.markdown('This application is a Streamlit dashboard for analyzing stock market picks')
with st.sidebar:
    
    

    ticker = st.text_input('Enter the ticker symbol', 'TSLA')
    start_year = 2021
    start_month = 1
    start_day = 1
   
    st.text('Loading...')

    
stock = ticker.upper()
if st.checkbox('Show stock data'):
    st.subheader(stock)
    
    #st.write(yf.Ticker(stock).history(start_year+'-'+start_month+'-'+start_day))
    
    start = dt.datetime(start_year, start_month, start_day)
    now = dt.datetime.now()

    df = pdr.get_data_yahoo(stock, start, now)
    st.write(df)

start = dt.datetime(start_year, start_month, start_day)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)
emasUsed = [3,5,8,10,12,15,30,35,40,45,50,60]
emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasUsed:
    if st.checkbox('Show EMA '+str(x)):
        st.subheader('EMA '+str(x))
        st.write(df.ewm(span=x, min_periods=x).mean())

emasUsed=[3,5,8,10,12,15,30,35,40,45,50,60]
for x in emasUsed:
    ema=x
    df["Ema_"+str(ema)]=round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

df=df.iloc[60:]

pos=0
num=0
percentchange=[]

for i in df.index:
	cmin=min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i],)
	cmax=max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i],)

	close=df["Adj Close"][i]
	
	if(cmin>cmax):
		print("Red White Blue")
		if(pos==0):
			bp=close
			pos=1
			print("Buying now at "+str(bp))


	elif(cmin<cmax):
		print("Blue White Red")
		if(pos==1):
			pos=0
			sp=close
			print("Selling now at "+str(sp))
			pc=(sp/bp-1)*100
			percentchange.append(pc)
	if(num==df["Adj Close"].count()-1 and pos==1):
		pos=0
		sp=close
		print("Selling now at "+str(sp))
		pc=(sp/bp-1)*100
		percentchange.append(pc)

	num+=1

print(percentchange)

gains=0
ng=0
losses=0
nl=0
totalR=1

for i in percentchange:
	if(i>0):
		gains+=i
		ng+=1
	else:
		losses+=i
		nl+=1
	totalR=totalR*((i/100)+1)

totalR=round((totalR-1)*100,2)

if(ng>0):
	avgGain=gains/ng
	maxR=str(max(percentchange))
else:
	avgGain=0
	maxR="undefined"

if(nl>0):
	avgLoss=losses/nl
	maxL=str(min(percentchange))
	ratio=str(-avgGain/avgLoss)
else:
	avgLoss=0
	maxL="undefined"
	ratio="inf"

if(ng>0 or nl>0):
	battingAvg=ng/(ng+nl)
else:
	battingAvg=0

st.subheader('Stock Return Analysis')
st.write('Total Return: '+str(totalR)+'%')
st.write('Average Gain: '+str(avgGain)+'%')
st.write('Average Loss: '+str(avgLoss)+'%')
st.write('Batting Average: '+str(battingAvg))
st.write('Max Gain: '+maxR+'%')
st.write('Max Loss: '+maxL+'%')
st.write('Gain/Loss Ratio: '+ratio)


#show 
			





