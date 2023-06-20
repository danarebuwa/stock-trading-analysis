import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

st.set_page_config(layout='wide')
st.title('Stock Market Dashboard')
st.sidebar.title('Input Parameters')

st.markdown('This application is a Streamlit dashboard for analyzing stock market picks. Enter your preferred stock and selection of EMAs to test your strategies.')
st.sidebar.markdown('Please enter the required details below:')

# Input Parameters
with st.sidebar:
    ticker = st.text_input('Enter the ticker symbol:', 'TSLA')
    start_year = st.number_input('Start Year', min_value=2000, max_value=dt.datetime.now().year, value=2021)
    start_month = st.selectbox('Start Month', options=range(1,13), index=0)
    start_day = st.selectbox('Start Day', options=range(1,32), index=0)
    selected_emas = st.multiselect('Select EMAs', options=[3,5,8,10,12,15,30,35,40,45,50,60], default=[3,5,8,10,12,15,30,35,40,45,50,60])

# Fetch Stock Data
stock = ticker.upper()
start = dt.datetime(start_year, start_month, start_day)
now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)

# Display Stock Data
if st.checkbox('Show raw stock data'):
    st.subheader('Raw Stock Data for ' + stock)
    st.dataframe(df)

# EMA Calculation
for ema in selected_emas:
    df["Ema_"+str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)

df=df.iloc[max(selected_emas):]

# Display EMA Data
for ema in selected_emas:
    if st.checkbox('Show EMA '+str(ema)):
        st.subheader('EMA '+str(ema) + ' for ' + stock)
        st.line_chart(df['Ema_'+str(ema)])

# Trading Strategy Implementation
# Trading Strategy Implementation
pos = 0
num = 0
percentchange = []

for i in df.index:
    ema_short = [df["Ema_"+str(ema)][i] for ema in selected_emas if ema <= 15]
    ema_long = [df["Ema_"+str(ema)][i] for ema in selected_emas if ema >= 30]

    if len(ema_short)==0 or len(ema_long)==0:  # Ensure there is at least one EMA selected in both short and long term
        continue

    cmin = min(ema_short)
    cmax = max(ema_long)
    close = df["Adj Close"][i]

    if(cmin>cmax):
        if(pos==0):
            bp=close
            pos=1

    elif(cmin<cmax):
        if(pos==1):
            pos=0
            sp=close
            pc=(sp/bp-1)*100
            percentchange.append(pc)

    if(num==df["Adj Close"].count()-1 and pos==1):
        pos=0
        sp=close
        pc=(sp/bp-1)*100
        percentchange.append(pc)

    num+=1


# Analyzing the Trading Strategy
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

# Display Trading Strategy Analysis
st.subheader('Stock Return Analysis')
st.write('Total Return: '+str(totalR)+'%')
st.write('Average Gain: '+str(avgGain)+'%')
st.write('Average Loss: '+str(avgLoss)+'%')
st.write('Batting Average: '+str(battingAvg))
st.write('Max Gain: '+maxR+'%')
st.write('Max Loss: '+maxL+'%')
st.write('Gain/Loss Ratio: '+ratio)




