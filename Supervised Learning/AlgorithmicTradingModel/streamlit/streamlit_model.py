# Imports the required libraries
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import financialanalysis as fa
import warnings
import streamlit as st
warnings.filterwarnings('ignore')

# Imports the data visualization libraries
import matplotlib.pyplot as plt
import hvplot.pandas
import holoviews as hv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
hv.extension('bokeh')

# Imports the machine learning modules
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

# Imports the data reporting modules
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


st.set_option('deprecation.showPyplotGlobalUse', False)
st.header('Algorithmic Trading Backtesting App')

st.markdown("""
This app pulls real-time price data for any stock ticker and backtests an algorithmic trading strategy based on desired buy/sell signals.
* **Python libraries:** pandas, numpy, os, streamlit,financialanalysis, scikit-learn
* **Data Source::** [YFinance](https://finance.yahoo.com/)
* **Models:** linear regression, logistic regression, random forest classification, support vector machine
* **Charts:** charts are interactive, expandable and downloadable
* **Buy/sell signals:** trendline, 1 standard deviation above/below, 2 standard deviations above/below
""")



# Sidebar header: stock and time period selection
st.sidebar.header('User Input Features')
st.sidebar.caption('Input any stock and timeframe, and choose your desired buy/sell signals for the bot.')

# Widget to select stock ticker
selected_asset = st.sidebar.text_input('Stock Ticker', value="SPY")

# Widget to select timeperiod
start_date = st.sidebar.date_input("Start Date", value = dt.date(2021, 11, 1), min_value = dt.date(2017, 1, 1)).strftime('%Y-%m-%d')
end_date = st.sidebar.date_input("End Date").strftime('%Y-%m-%d')

buy_signal = st.sidebar.selectbox('Buy Signal', ("Trendline", "1 Standard Deviation (Above)", "1 Standard Deviation (Below)", "2 Standard Deviations (Above)", "2 Standard Deviations (Below)"))
sell_signal = st.sidebar.selectbox('Sell Signal', ("Trendline", "1 Standard Deviation (Above)", "1 Standard Deviation (Below)", "2 Standard Deviations (Above)", "2 Standard Deviations (Below)"))

# YFinance API pull
pull = yf.Ticker(f"{selected_asset}")
data = pull.history(start = start_date, end = end_date)
data = pd.DataFrame(data["Close"])       
data = data.rename(columns={"Close": "Price"})

# Calculates daily returns and cumulative returns
data["Daily Returns"] = data["Price"].pct_change().dropna()
data["Cumulative Returns"] = (1 + data["Daily Returns"]).cumprod()
data = data.dropna()

# Standard deviation of cumulative returns
std = data["Cumulative Returns"].std()

# Copies DataFrame for the machine learning models
model_df = data
model_df.reset_index(inplace=True)
model_df.dropna(inplace=True)

# Builds the timeseries linear regression trendlinea
X = model_df["Date"].to_list() # converts Series to list
X = fa.datetimeToFloatyear(X) # for example, 2020-07-01 becomes 2020.49589041
X = np.array(X) # converts list to a numpy array
X = X[::,None] # converts row vector to column vector (just column vector is acceptable)
y = model_df["Cumulative Returns"] # get y data (relative price)
y = y.values # converts Series to numpy
y = y[::,None] # row vector to column vector (just column vector is acceptable)
 
slope, intercept, x, fittedline = fa.timeseriesLinearRegression(model_df["Date"], model_df["Cumulative Returns"])

# Creates standard deviation parallel channels from trendline
std_1_upper = fittedline + std
std_1_lower = fittedline - std
std_2_upper = fittedline + (std*2)
std_2_lower = fittedline - (std*2)

# Adds the trendlines to the model DataFrame
model_df["Trendline"] = fittedline
model_df["1 Standard Deviation (Above)"] = std_1_upper
model_df["1 Standard Deviation (Below)"] = std_1_lower
model_df["2 Standard Deviations (Above)"] = std_2_upper
model_df["2 Standard Deviations (Below)"] = std_2_lower

model_df.index = model_df["Date"]
model_df = model_df.drop(columns="Date")

# Initializes the trade Signal column
model_df['Signal'] = 0.0

# When Price is less than or equal to the mean, generates signal to buy stock long
model_df.loc[(model_df['Cumulative Returns'] < model_df[f"{buy_signal}"]), 'Signal'] = 1

# When Price is one standard deviation above the mean, generates signal to sell stock short
model_df.loc[(model_df['Cumulative Returns'] > model_df[f"{sell_signal}"]), 'Signal'] = -1

# Calculates the strategy returns and add them to the signals_df DataFrame
model_df['Strategy Returns'] = (1 + (model_df['Daily Returns'] * model_df['Signal'].shift().dropna())).cumprod()

model_df = model_df.dropna()


# Creates the target set selecting the Signal column and assiging it to y
y = model_df[["Signal"]]

# Creates the model inputs by dropping Signal & Strategy Returns columns and assigning it to X
X = model_df[["Trendline", "1 Standard Deviation (Above)", "1 Standard Deviation (Below)", "2 Standard Deviations (Above)", "2 Standard Deviations (Below)"]]

# Checks the y values to determine if oversampling is needed
y.value_counts()
X.dropna(inplace=True)

# Splits the data using train_test_split and assigns a random_state of 1 to the function
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# Creates a StandardScaler instance
scaler = StandardScaler()

# Applys the scaler model to fit the X-train data
X_scaler = scaler.fit(X_train)

# Transforms the X_train and X_test DataFrames using the X_scaler
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)

# Instantiates the random oversampler model with a random_state parameter of 1
random_oversampler = RandomOverSampler(random_state=1)

# Fits the original training data to the random_oversampler model
X_resampled, y_resampled = random_oversampler.fit_resample(X_train, y_train)

# Checks the resamped y values
y_resampled.value_counts()


# Creates a LogisticRegression model and trains it on the X_train_scaled and y_resampled
regression_model = LogisticRegression()
regression_model.fit(X_resampled, y_resampled)

# Uses the model you trained to predict using X_test_scaled
lr_pred = regression_model.predict(X_test_scaled)

# Creates a classification report to evaluate performance and saves it
regression_testing_report = classification_report(y_test, lr_pred, digits=4)

# Creates a RandomForestClassifier model and trains it on the X_train_scaled
forest_model = RandomForestClassifier(random_state=0)

# Uses the model you trained to predict using X_test_scaled
forest_model.fit(X_resampled, y_resampled)
rfc_pred = forest_model.predict(X_test_scaled)

# Creates a classification report to evaluate performance and saves it
forest_testing_report = classification_report(y_test, rfc_pred, digits=4)


# From SVM, instantiates SVC classifier model instance
svm_model = svm.SVC()
 
# Fits the model to the data using the training data
svm_model = svm_model.fit(X_resampled, y_resampled)
 
# Uses the testing data to make the model predictions
svm_pred = svm_model.predict(X_test_scaled)

# Creates a classification report to evaluate performance and saves it
svm_testing_report = classification_report(y_test, svm_pred, digits=4)


# Creates a predictions DataFrame
predictions_df = pd.DataFrame(index=X_test.index)

# Adds the model predictions to the DataFrame
predictions_df['LR Predicted'] = lr_pred
predictions_df['SVM Predicted'] = svm_pred
predictions_df['RFC Predicted'] = rfc_pred

# Adds the actual returns to the DataFrame
predictions_df['Daily Returns'] = model_df['Daily Returns']
predictions_df['Actual Returns'] = model_df['Cumulative Returns']
predictions_df['Strategy Returns'] = model_df['Strategy Returns']

# Adds the strategy returns (daily) to the DataFrame
predictions_df['LR Daily Returns'] = (predictions_df['Daily Returns'] * predictions_df['LR Predicted'])
predictions_df['RFC Daily Returns'] = (predictions_df['Daily Returns'] * predictions_df['RFC Predicted'])
predictions_df['SVM Daily Returns'] = (predictions_df['Daily Returns'] * predictions_df['SVM Predicted'])

# Converts the strategy returns from daily to cumulative
predictions_df['LR Strategy Returns'] = (1 + predictions_df['LR Daily Returns']).cumprod()
predictions_df['RFC Strategy Returns'] = (1 + predictions_df['RFC Daily Returns']).cumprod()
predictions_df['SVM Strategy Returns'] = (1 + predictions_df['SVM Daily Returns']).cumprod()

predictions_df = predictions_df.drop(columns=['LR Daily Returns', 'RFC Daily Returns', 'SVM Daily Returns'])


returns_graph = predictions_df[["Actual Returns", "Strategy Returns",
                "LR Strategy Returns", 
                "RFC Strategy Returns", 
                "SVM Strategy Returns"]].hvplot.line(hover_color="black", legend="top_left", rot=45)

st.bokeh_chart(hv.render(returns_graph, backend="bokeh"))   
