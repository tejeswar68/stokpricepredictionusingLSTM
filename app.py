
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import tensorflow.compat.v2 as tf
import yfinance as yf
from PIL import Image
from keras.models import load_model
import streamlit as st

start= '2015-01-01'
end= '2022-12-05'

st.title('Stock Price Prediction')

user_input= st.text_input('Enter Stock Ticker', 'SBIN.NS')
df= yf.download(user_input, start ,end , prepost = True,  progress=False)

#list of stock tickers
st.subheader('YAHOO STOCK TICKERS OF SOME TOP COMPANIES! ')

st.json({
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "Amazon.com, Inc.": "AMZN",
    "Alphabet Inc. (Google)": "GOOGL",
    "Facebook, Inc.": "FB",
    "Berkshire Hathaway Inc.": "BRK-A",
    "Johnson & Johnson": "JNJ",
    "Visa Inc.": "V",
    "Procter & Gamble Co.": "PG",
    "JPMorgan Chase & Co.": "JPM",
    "Tesla, Inc.": "TSLA",
    "Walmart Inc.": "WMT",
    "Johnson Controls International plc": "JCI",
    "Coca-Cola Company (The)": "KO",
    "Visa Inc.": "V",
    "Mastercard Incorporated": "MA",
    "NVIDIA Corporation": "NVDA",
    "Walt Disney Company (The)": "DIS",
    "Netflix, Inc.": "NFLX",
    "PayPal Holdings, Inc.": "PYPL",
    "Adobe Inc.": "ADBE",
    "Salesforce.com, Inc.": "CRM",
    "Cisco Systems, Inc.": "CSCO",
    "Intel Corporation": "INTC",
    "Advanced Micro Devices, Inc.": "AMD"
}
)



# Describing Data
st.subheader('Data from 2015 - 2022')
st.write(df.describe())

# Visualization
st.subheader('Closing Price v/. Time Chart')
fig= plt.figure(figsize= (12, 8))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price v/. Time Chart with 100MA')
ma100= df.Close.rolling(100).mean()
fig= plt.figure(figsize= (12, 8))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price v/. Time Chart with 100MA and 200MA')
ma200= df.Close.rolling(200).mean()
fig= plt.figure(figsize= (12, 8))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)

# Splitting CLosing Price Data into Training and Testing
data_training= pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing= pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler(feature_range= (0, 1))

data_training_array= scaler.fit_transform(data_training)

# Loading our model
model= load_model('keras_model001.h5')

# Testing Part
past_100_days= data_training.tail(100) # appending the past 100 days to data_testing.
final_df= past_100_days.append(data_testing, ignore_index= True)
input_data= scaler.fit_transform(final_df)

x_test= []
y_test= []

for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i-100: i])
  y_test.append(input_data[i, 0]) # the 0th column of ith row.

x_test, y_test= np.array(x_test), np.array(y_test)
y_predicted= model.predict(x_test)

scaler= scaler.scale_ # the factor by which we shall scale the data up
scale_factor= 1/scaler[0]
y_predicted= y_predicted * scale_factor
y_test= y_test * scale_factor

# Final Graph
st.subheader('Predicted v/. Original')
fig2= plt.figure(figsize= (12, 8))
plt.plot(y_test, 'blue', label= 'Original Closing Price')
plt.plot(y_predicted, 'orange', label= 'Predicted Closing Price')
plt.xlabel('Timeline')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)


st.write("<h1 style='text-align: center;'>AUTHORS</h1>", unsafe_allow_html=True)


teja = Image.open("profilePic/teja.jpg")
saket = Image.open("profilePic/saket.jpg")
pavan= Image.open("profilePic/pavan.jpg")

# Display images in a row
col1, col2, col3 = st.columns(3)
with col1:
    st.image(teja, caption="Tejeswara Murthy Palwadi", use_column_width=True)
with col2:
    st.image(saket, caption="Palarapu Saket", use_column_width=True)
with col3:
    st.image(pavan, caption="Guda Pavaneeshwar Reddy", use_column_width=True)
