#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries
import math
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data
stock = data.DataReader('DIA', 'yahoo',start='1/1/1999')
stock.head()
plt.style.use('seaborn-pastel')


# In[17]:


#Calculate the number of days elapsed in our chosen time window
time_elapsed = (stock.index[-1] - stock.index[0]).days
print(time_elapsed)


# In[18]:


#Current price / first record (e.g. price at beginning of 1999) provides us with the total growth %
price_ratio = (stock['Adj Close'][-1] / stock['Adj Close'][1])
#Annualize this percentage
#Convert our time elapsed to the # of years elapsed
inverse_number_of_years = 365.0 / time_elapsed
#Raise the total growth to the inverse of the # of years (e.g. ~1/10 at time of writing) to annualize our growth rate
cagr = price_ratio ** inverse_number_of_years - 1
print(cagr)


# In[19]:


#Mean annual growth rate above.

#Calculate the standard deviation of the daily price changes
vol = stock['Adj Close'].pct_change().std()
print(vol)


# In[20]:


#Roughy ~252 trading days in a year, scale this by an annualization factor
number_of_trading_days = 252
vol = vol * math.sqrt(number_of_trading_days)


# In[21]:


#Two inputs needed to generate random values in our simulation
print ("cagr (mean returns) : ", str(round(cagr,4)))
print ("vol (standard deviation of return : )", str(round(vol,4)))


# In[22]:


#Generate random values for 1 year's worth of trading (252 days),using numpy and assuming a normal distribution
daily_return_percentages = np.random.normal(cagr/number_of_trading_days, vol/math.sqrt(number_of_trading_days),number_of_trading_days)+1


# In[23]:


#Random series of future daily return %s above, apply these forward-looking to our last stock price in the window, 
#effectively carrying forward a price prediction for the next year

#This distribution is known as a 'random walk'
price_series = [stock['Adj Close'][-1]]

for drp in daily_return_percentages:
    price_series.append(price_series[-1] * drp)


# In[24]:


#Plot of single 'random walk' of stock prices 
plt.plot(price_series)
plt.show()


# In[25]:


#Random walk above
#Simulate this process over a large sample size to get a better sense of the true expected distribution
number_of_trials = 1000

#Set up an additional array to collect all possible closing prices in last day of window. 

#Calculate randomized return percentages following our normal distribution and using the mean / std dev we calculated above
for i in range(number_of_trials):
    daily_return_percentages = np.random.normal(cagr/number_of_trading_days, vol/math.sqrt(number_of_trading_days),number_of_trading_days)+1
    price_series = [stock['Adj Close'][-1]]

#Extrapolate price out for next year
    for drp in daily_return_percentages: 
        price_series.append(price_series[-1] * drp)
    
#Plot all random walks
    plt.plot(price_series)
plt.show()


# In[26]:


#Same as above but with a bigger number of trials, and an added histogram
ending_price_points = []
larger_number_of_trials = 10000 
for i in range(larger_number_of_trials):
    daily_return_percentages = np.random.normal(cagr/number_of_trading_days, vol/math.sqrt(number_of_trading_days),number_of_trading_days)+1
    price_series = [stock['Adj Close'][-1]]

    for drp in daily_return_percentages:
        price_series.append(price_series[-1] * drp)
    
    plt.plot(price_series)
    
    ending_price_points.append(price_series[-1])

plt.show()

plt.hist(ending_price_points,bins=50)
plt.show()


# In[27]:


#Check the mean of all ending prices and arrive at the most probable ending point
expected_ending_price_point = round(np.mean(ending_price_points),2)
print("Expected Ending Price Point : ", str(expected_ending_price_point))


# In[31]:


#Sample mean, Population Mean, and Percent Difference
population_mean = (cagr+1) * stock['Adj Close'][-1]
print ("Sample Mean : ", str(expected_ending_price_point))
print ("Population Mean: ", str(round(population_mean,2)));
print ("Percent Difference : ", str(round((population_mean - expected_ending_price_point)/population_mean * 100,2)), "%")


# In[32]:


#Split the distribution into percentiles to help us gauge risk vs. reward

#Pull top 10% of possible outcomes
top_ten = np.percentile(ending_price_points,100-10)
#Pull bottom 10% of possible outcomes
bottom_ten = np.percentile(ending_price_points,10);
print ("Top 10% : ", str(round(top_ten,2)))
print ("Bottom 10% : ", str(round(bottom_ten,2)))


# In[33]:


#Create histogram again
plt.hist(ending_price_points,bins=100)
#Append with top 10% line
plt.axvline(top_ten,color='r',linestyle='dashed',linewidth=2)
#Append with bottom 10% line
plt.axvline(bottom_ten,color='r',linestyle='dashed',linewidth=2)
#Append with current price
plt.axhline(stock['Adj Close'][-1],color='g', linestyle='dashed',linewidth=2)
plt.show()


# In[ ]:




