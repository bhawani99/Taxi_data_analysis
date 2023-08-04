#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import important libraries - matplotlib, seaborn and pandas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# 
# # Yellow Taxi Feb data

# ## Data Importing and Data Summarisation

# In[ ]:


# yellow taxi data
file_loc1 = '/content/drive/MyDrive/Data/yellow_tripdata_2020-02.csv'

# read file
trip_data = pd.read_csv(file_loc1)
trip_data.head()


# In[ ]:


trip_data.info()


# In[ ]:


trip_data.shape


# ## Data Cleaning and Manipulation Steps

# In[ ]:


#removing unwanted columns
trip_data.drop(['Unnamed: 0','VendorID','RatecodeID','store_and_fwd_flag','airport_fee','congestion_surcharge'],inplace = True,axis =1)


# In[ ]:


#converting object to datetime object
trip_data['tpep_pickup_datetime'] = pd.to_datetime(trip_data['tpep_pickup_datetime'])
trip_data['tpep_dropoff_datetime'] = pd.to_datetime(trip_data['tpep_dropoff_datetime'])


# In[ ]:


trip_data.info()


# In[ ]:


# droping nan values
trip_data = trip_data.dropna()


# In[ ]:



# create 'duration' column using pd.Timedelta(minutes=1)
trip_data['duration'] = (trip_data['tpep_dropoff_datetime'] - trip_data['tpep_pickup_datetime'])/ pd.Timedelta(minutes=1)
# create 'trip_pickup_hour' column using 'tpep_pickup_datetime' column
trip_data['trip_pickup_hour'] = trip_data['tpep_pickup_datetime'].dt.hour
# create 'trip_dropoff_hour' column using 'tpep_dropoff_datetime' column
trip_data['trip_dropoff_hour'] = trip_data['tpep_dropoff_datetime'].dt.hour
# create 'trip_day' column using 'tpep_pickup_datetime' column - use day_name()
trip_data['trip_day'] = trip_data['tpep_pickup_datetime'].dt.day_name()
# print data info
print(trip_data.info())
# print data head
trip_data.head()


# Now our Total_amount is basically Total_amount = fare_amount + tolls_amount + tip_amount + (extra + mta_tax + improvement_surcharge)
# 
# of the above components of total_amount we will specifically focus on 'fare_amount','tip_amount', 'tolls_amount' and 'total taxes'.

# In[ ]:


#combining the all taxes to one, then drop that columns  
trip_data['total_tax'] = trip_data['extra'] + trip_data['mta_tax'] + trip_data['improvement_surcharge'] 
trip_data.drop(['extra','mta_tax','improvement_surcharge'],inplace = True,axis = 1)


# In[ ]:


# covert passenger count to int, float does not make sense
trip_data['passenger_count']=trip_data['passenger_count'].astype(int)


# For payment_type we have the following mapping for categories: 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip
# 
# let's just check if we have only these categories available in payment_type or not

# In[ ]:


# value_counts for 'payment_type' column
trip_data['payment_type'].value_counts()


# In[ ]:


def map_payment_type(x):
    if x==1:
        return 'Credit_card'
    elif x==2:
        return 'Cash'
    elif x==3:
        return 'No_charge'
    elif x==4:
        return 'Dispute'
    elif x==5:
        return 'Unknown'
    else:
        return 'Voided_trip'

# use .apply and lambda on payment_type column to change 'payment_type' column
trip_data['payment_type'] = trip_data.payment_type.apply(lambda x:map_payment_type(x))
# print data head
trip_data.head()


# In[ ]:


#Save to cleaned csv
trip_data.to_csv('/content/drive/MyDrive/Data/yellow_tripdata_2020-02_cleaned.csv',index=False)


# ## Data Analysis and Visualisation

# In[ ]:


# yellow taxi data
file_loc1 = '/content/drive/MyDrive/Data/yellow_tripdata_2020-02_cleaned.csv'

# read file
trip_data = pd.read_csv(file_loc1)
trip_data.head()


# 
# 
# ### Univariate Analysis

# CONTINUOUS VARIABLE DISTRIBUTION

# In[ ]:


# continuous_columns list
continuous_columns = ['fare_amount','tip_amount','total_tax','total_amount','duration','trip_distance','tolls_amount']


# In[ ]:


trip_data[continuous_columns].head()


# In[ ]:


# use .describe() for showing the statistics for continuous columns
trip_data[continuous_columns].describe()


# Since we are trying to understand the distribution of continuous numerical variables, we will be using
# 
# histograms box plots Below we have used a for loop to loop through all the continuous variables and then draw histograms and box plots for each of them at each iteration

# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# Negtive values for columns does not make sense fare_amount tip_amount total_taxes tolls_amount total_amount duration
# 
# Let's just observe how the negative values in each of these columns look like

# In[ ]:


trip_data.loc[trip_data['fare_amount']<0]


# In[ ]:


trip_data.loc[trip_data['tip_amount']<0]


# In[ ]:


trip_data.loc[trip_data['tolls_amount']<0]


# In[ ]:


trip_data.loc[trip_data['total_tax']<0]


# In[ ]:


trip_data.loc[trip_data['total_amount']<0]


# In[ ]:


#droping negative values
trip_data = trip_data.loc[trip_data['fare_amount']>=0]
trip_data = trip_data.loc[trip_data['tip_amount']>=0]
trip_data = trip_data.loc[trip_data['tolls_amount']>=0]
trip_data = trip_data.loc[trip_data['total_tax']>=0]
trip_data = trip_data.loc[trip_data['total_amount']>=0]
trip_data = trip_data.loc[trip_data['duration']>=0]


# In[ ]:


trip_data.shape


# Now we will again look at the distribution plots for these variables

# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# In[ ]:


# use .describe() again to show the statistics for these continuous variables
trip_data[continuous_columns].describe()


# we need to improve the look of histograms and box plots further as we are not able to clearly observe the distribution.
# 
# We will filter all the data for each feature with values less than 95% ile. Then plot that data as shown below

# In[ ]:


trip_data.to_csv('/content/drive/MyDrive/Data/yellow_tripdata_2020-02_cleaned.csv',index=False)


# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    # removing the outliers
    feature_data_percentile = trip_data[feature].quantile(0.95)
    feature_data = trip_data.loc[trip_data[feature]<feature_data_percentile,feature]
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(feature_data)
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(feature_data,ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# Looking from the above histograms and box plots we can decipher following information for each column
# 
# fare_amount - most of the fare amount is within 9 dollar value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 6000 dollars.
# 
# tip_amount - most of the tip amount is within 2 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 560 dollars.
# 
# tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.
# 
# total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. Though we have outliers in this case but it is not as signiificant as the case for tip and fare.
# 
# total_amount - most of the total_amount values is within 14.5 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.
# 
# duration - most of the values in duration is within 12 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 3000 minutes.
# 
# trip_distance - most of the trip_distance is within 1.60 miles value as is shown by the median. The outlier in this case is about 350 miles.

# In[ ]:


#univarient analysis for categorical coloumns
categorical_variables = ['payment_type','trip_pickup_hour','trip_dropoff_hour','trip_day','PULocationID','DOLocationID']


# In[ ]:


# start exploration with payment_type using .value_counts()
trip_data['payment_type'].value_counts()


# In[ ]:


# but this is a series for ease of plotting we need to use dataframe using .reset_index() on value_counts()
payment_type_category_count = trip_data['payment_type'].value_counts().reset_index()
# print the above dataframe
payment_type_category_count


# In[ ]:


# we are shown the count under each category but it is better to have count% for comparison - create count_percent col
payment_type_category_count['count_percent'] = (payment_type_category_count['payment_type']/trip_data.shape[0])*100
# print the data frame
payment_type_category_count


# In[ ]:


# now let's plot it as bar chart
# first step - create fig, ax object using plt.subplots
fig,ax = plt.subplots(figsize=(7,7))
# second step - use sns.barplot(x, y , data, ax) for plotting bar plot
sns.barplot(x = 'index', y = 'count_percent', data=payment_type_category_count,ax=ax)
# third step - use ax object to change plot properties - here we set a title with ax.set_title()
ax.set_title('box plot for payment_type column')
# third step - seaborn style setting
sns.set()
# fourth step - use plt.show() for showing the plots
plt.show()


# From above we can understand that most of the payments are done through cash and credit cards. The proportion of credit card payments is around 70%.
# 
# Now we look into time based categorical variables.
# 
# 'trip_pickup_hour' 'trip_dropoff_hour' 'trip_day'

# In[ ]:


# now let's plot all the time based categorical variables in this way using a for loop
for feature in ['trip_pickup_hour','trip_dropoff_hour','trip_day']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    if feature_value_counts.shape[0]<10:
        fig,ax = plt.subplots(figsize=(7,7))
    else:
        fig,ax = plt.subplots(figsize=(20,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# Based on above plots we can observe following things
# 
# Trip Hour 1) The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 11 min.
# 
# 2) Peak hour for the pick up and drop off is around evening from 5 to 7. The busiest time is 6PM.
# 
# 3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.
# 
# Trip day
# 
# 1)Sunday has the lowest taxi uses while saturday is the busiest.
# 
# 2)Weekdays except Monday have heavy taxi uses.

# Moving on we will explore the distribution of location based features:
# 
# 'PULocationID'
# 
# 'DOLocationID'

# In[ ]:


# let's see the number of categories available in both pickup and dropoff location - PULocationID and DOLocationID
print(trip_data['PULocationID'].value_counts().shape)
print(trip_data['DOLocationID'].value_counts().shape)


# So we have around 260 categories for location. To plot it on bar plots we need to increase the figure size.

# In[ ]:


for feature in ['PULocationID','DOLocationID']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    fig,ax = plt.subplots(figsize=(25,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# The above plots looks quite messy but one insight that we can indetify from above plot that most of pickup and dropoff points do not have more 0.5% traffic (0.5 percent of 8755612 total trips is 43778).
# 
# So in our next plot we will filter out these pickup and dropoff points to look into the graph more clearly.

# In[ ]:


for feature in ['PULocationID','DOLocationID']:
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # filter only those location which has more than 0.5 % of traffic
    feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.5]
    print('Number of categories in feature '+ feature + ' above 0.5 % count is ' + str(feature_value_counts.shape[0]))
    fig,ax = plt.subplots(figsize=(25,7))
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    ax.set_title('Bar plot for '+ feature)
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# From the above plots we can glance following insights
# 
# The busiest location in terms of pickup are 161, 237 and 236
# 
# The busiest location for dropoff too are 236 , 237 and 161 but order is some what different.
# We can also look for routes which are busiest.
# 
# For exploring busy routes we need to create a new route column which is a combination of pickup and dropoff point.
# 
# So route = 'PULocationID'-'DULocationID'

# In[ ]:


# create routes column using PULocationID and DOLocationID with lambda function
trip_data['routes'] = trip_data.apply(lambda x: str(x['PULocationID'])+'-'+str(x['DOLocationID']),axis=1)


# In[ ]:


trip_data['routes'].head()


# In[ ]:


trip_data.info()


# In[ ]:


trip_data.to_csv('/content/drive/MyDrive/Data/yellow_tripdata_2020-02_cleaned.csv',index=False)


# In[ ]:


# plot bar plot for routes which have trip count above 0.25%
feature = 'routes'
feature_value_counts = trip_data[feature].value_counts().reset_index()
feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
# choosing routes where the trip percent is above 0.25% of total trips
feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.25]
print('Number of categories in feature '+ feature + ' above 0.25 % count is ' + str(feature_value_counts.shape[0]))
fig,ax = plt.subplots(figsize=(25,7))
sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
ax.set_title('Bar plot for '+ feature)
ax.set_xlabel(feature)
sns.set()
plt.show()


# From the above plot we can observe that 5 busiest route are following:
# 
# 237-236
# 
# 236-236
# 
# 236-237
# 
# 237-237

# In[ ]:


# Analysis for passenger count
trip_data['passenger_count'].value_counts()


# Here we see that the mostly 1 or 2 passengers avail the cab. The instance of large group of people travelling together is rare.

# ### Bivariate Analysis

# Remember that we made some analysis points regarding exploration of duration and pricing:
# 
# For pricing we will be exploring it's relationship with:
# 
# hour/day of trip
# 
# pickup location of trip
# 
# For duration we will be exploring it's relationship with:
# 
# hour of day
# 
# pickup location of trip
# 
# PRICING EXPLORATION
# 
# We have following variables in the dataset that is associated with pricing:
# 
# fare_amount
# 
# tip_amount
# 
# total_taxes
# 
# tolls_amount
# 
# total_amount
# 
# In our anlaysis for now we will be focussing on:
# 
# fare_amount
# 
# tip_amount
# 
# total_taxes
# 
# total_amount
# 
# we are leaving tolls_amount for now from our analysis as it contributes very little to the total_amount value because it's median value was 0 i.e. most of the trips are not paying tolls_amount.
# 
# PRICING VARIABLE EXPLORATION WITH HOUR/DAY OF TRIP *
# All of our pricing variables are continuous and Hour/Day is categorical.
# 
# The way to explore relationship between a continuous variable and categorical variable is through a box plot. We create box plot for each category of categorical variable.
# 
# so as to see how the distribution changes for the continuous variables as the category values changes for categorical variable.
# 
# We will start with fare_amount exploration.
# 
# Let's do a box plot of fair_amount with hour/day of trip to see how the fare changes for different hours of the day and for different days of the week

# In[ ]:


# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()


# In[ ]:


# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()


# From the above plot we can observe that most of the outliers in fare happens during 14 or 2PM to 18 or 6PM based on pickup time.
# 
# From the above plot trip_dropoff_hour outliers happens during 15 or 3PM to 19 or 7PM based on pickup time.
# 
# For observing the distribution in a better way we would restrict the fare_amount to below 50 dollars.

# In[ ]:


# restricted_fare_amount_data dataframe formation by filtering fare_amount less than 50 dollars
restricted_fare_amount_data = trip_data.loc[(trip_data['fare_amount']<=50) & (trip_data['fare_amount']>=0)]
restricted_fare_amount_data.shape


# In[ ]:


#now plot graph for restricted data
fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()


# We can see from the plots that trip pickup and dropoff hours do not have much affect on median fare_amount as median is almost same for all the hours.(but fare amount between 5 A.M to 6 A.M is little less than the remaining hour)
# 
# let's us see if hour of day has any effect on other pricing related variables or not.
# 
# Starting with total_amount

# In[ ]:


restricted_tip_amount_data = trip_data.loc[trip_data['tip_amount']<10]
restricted_total_taxes_data = trip_data.loc[trip_data['total_tax']<10]


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()


# Based on tip_amount plot we can see that tip_amount too does not vary much based on hours. but one pattern we can say that tip is llittle large at late nights as compared to early mornings
# 
# Let's observe total_taxes now

# In[ ]:


# total_taxes = extra + improvement_surcharges + Mta

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='total_tax',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='total_tax',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()


# Now in this plot we can clearly observe that total_taxes change significantly with hour of the day.
# 
# There are two patterns that we can observe here:
# 
# 1)from the hour 8PM to 5AM the median taxes seem to be a bit higher than other hours, it may be due to some overnight surcharges.
# 
# 2) Evening from 4PM to 7PM have quite variable taxes and is a bit higher than other times, it may be due to higher traffic charges.
# 
# Overall the effect of hour of day is most clearly visible on total_taxes. we have two insights about how taxes change with hours
# 
# 1)Overnight charges are applied between 8PM to 5AM
# 
# 2)Evening has higher variability in taxes and the taxes are usually high.
# 
# Let's move and explore the distribution of pricing variables with respect to day of week. For this analysis we will be using restricited version of dataset that we built for fare_amount, total_amount, tip_amount and total_taxes.

# In[ ]:


# plot of trip_day with fare_amount
fig,ax = plt.subplots(figsize=(7,7))
# changes in sns.boxplot x and y
sns.boxplot(x = 'trip_day',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt the day of the week')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt the day of the week')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='total_tax',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt the day of the week')
sns.set()
plt.show()


# We can see that pricing overall does not change much with respect to day of week.
# 
# PRICING VARIABLE EXPLORATION WITH LOCATION OF TRIP *
# Here we will look into the price changes for the most frequent trip pickup locations.

# In[ ]:


# create a new series using value_counts() on 'PULocationID'
pickup_location_value_counts = trip_data['PULocationID'].value_counts()
# show the series
pickup_location_value_counts.head()


# In[ ]:


# top 10 frequent pickup locations using .nlargest(10).index
top_10_frequent_pickup_locations = pickup_location_value_counts.nlargest(10).index
top_10_frequent_pickup_locations


# In[ ]:


# for loop for plotting box plot of each of the top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median fare_amount for the top_pickup_locID
    print('The median fare_amount of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['fare_amount'].median()))
    # fig,ax object
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of fare_amount from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()


# So from above plot we can observe that for one of the most busiest pickup location i.e 161 has median fare_amount is low in comparison to other 186 locations ID and also oultier of 186 location ID is also high.and also we have location ID 162 and 230 has same fare amount as 161
# 
# This could be helpful in adjusting our revenue expectation based on putting our cabs in a given location because just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.

# ### Duration Exploaration

# Here we will explore the duration of trip exploration with pickup hour of day.

# In[ ]:


# plot box plot for duration for different hours of day
fig,ax = plt.subplots(figsize=(20,7))
# box plot using sns.boxplot x is 'trip_pickup_hour' and y is 'duration'
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = trip_data,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()


# Here again due to heavy outliers in duration data we are not able to observe the general graph. we might need to restrict our duration values to within 50min.

# In[ ]:


# create restricted_duration dataframe with .loc on 'duration' column
restricted_duration= trip_data.loc[trip_data['duration']<50]
restricted_duration.shape


# In[ ]:


fig,ax = plt.subplots(figsize=(20,7))
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = restricted_duration,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()


# Early morning hours of 5AM to 6AM have shorter duration trips

# In[ ]:


# plot box plots of duration for top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median duration for the top_pickup_locID
    print('The median trip duration of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['duration'].median()))
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()


# Here again we can see for the most frequent pickup location 161 the duration value is less in comparison to other pickup location with locationID 186, 186 has higher duration thats why it median far_amount is also higher.

# ### Analyse routes

# We could analyse routes with fare_amount or total_taxes and duration for different time of the day.

# In[ ]:


trip_data.head()


# In[ ]:


trip_route_value_counts = trip_data['routes'].value_counts()


# In[ ]:


trip_route_value_counts.head(10)


# In[ ]:


trip_route_top_10 = trip_route_value_counts.nlargest(10).index


# In[ ]:


trip_route_top_10 


# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median fare_amount for the respective route
    print("the fare amount for the route " + trip_route +' '+ 'is ' + str(trip_route_df['fare_amount'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()


# From above plot it is clear that the busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is bit lower than the other Busiset trip_routes.
# 
# It is also clearly vissible that the route 161-237 has higher median fare amount compared to other routes and its outliers are also low.
# 
# the trip_route 264-264 has the highest fare_amount of 9.5 median.Its worthnoting that these route should be kept in mind for business prospect.

# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the total_taxes for the route " + trip_route +' '+ 'is ' + str(trip_route_df['total_tax'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['total_tax'],ax=ax)
    # set_title
    ax.set_title('box plot of total_taxes for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()


# From the above plot it is clearly vissible almost all routes has same total_tax of 1.3 dollars, but the trip_route 264-264 total_tax i.e .8 dollars as well.
# 
# As we seen from fare_amount plot of routes, the 161-237 route has higher fare amount as compared to other routes but it could be higher because of higher taxes applied on the these route as shown in above plot. as it has highest total_tax value of 1.8 dollars

# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the duration for the route " + trip_route +' '+ 'is ' + str(trip_route_df['duration'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe  trip_route_df 
    sns.boxplot(trip_route_df['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for trip_route '+ trip_route)
    sns.set()
    plt.show()


# As seen from the above plot that the busisest location 237-236 has lower duration as compared other busisest location.
# 
# On the other hand 264-264 has higher duration and that could be the reason for the higher fare_amount.

# ## Final Results from EDA 

# fare_amount - most of the fare amount is within 9 dollar value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 6000 dollars.
# 
# tip_amount - most of the tip amount is within 2 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 560 dollars.
# 
# tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.
# 
# total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. Though we have outliers in this case but it is not as signiificant as the case for tip and fare.
# 
# total_amount - most of the total_amount values is within 14.5 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.
# 
# duration - most of the values in duration is within 12 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 3000 minutes.
# 
# trip_distance - most of the trip_distance is within 1.60 miles value as is shown by the median. The outlier in this case is about 350 miles.
# 
# Credit card is the most preferred mode of payment followed by cash.
# 
# Trip Hour-1)The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 11 min.
# 
# 2) Peak hour for the pick up and drop off is around evening from 5 to 7. The busiest time is 6PM.
# 
# 3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.
# 
# Trip day
# 
# Sunday has the lowest taxi uses while saturday is the busiest.Weekdays except Monday have heavy taxi uses.
# 
# The busiest location in terms of pickup are 161, 237 and 236
# 
# The busiest location for dropoff too are 236 , 237 and 161 but order is some what different. We can also look for routes which are busiest.
# 
# Here we see that the mostly 1 or 2 passengers avail the cab.
# 
# From the hour 8PM to 5AM the median taxes seem to be a bit higher than other hours, it may be due to some overnight surcharges.
# 
# Evening from 4PM to 7PM have quite variable taxes and is a bit higher than other times, it may be due to higher traffic charges.
# 
# We discovered from the dataset that even for the busiest pickup location the median fare_amount is a lower than other busier pickup locations. So just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.
# 
# Early morning hours of 5AM to 6AM have shorter duration trips
# 
# Routes:
# 
# From above plot it is clear that the busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is bit lower than the other Busiset trip_routes.
# 
# It is also clearly vissible that the route 161-237 has higher median fare amount compared to other routes and its outliers are also low.
# 
# the trip_route 264-264 has the highest fare_amount of 9.5 median.Its worthnoting that these route should be kept in mind for business prospect.
# 
# From the above plot it is clearly vissible almost all routes has same total_tax of 1.3 dollars, but the trip_route 264-264 total_tax i.e .8 dollars as well.
# 
# As we seen from fare_amount plot of routes, the 161-237 route has higher fare amount as compared to other routes but it could be higher because of higher taxes applied on the these route as shown in above plot. as it has highest total_tax value of 1.8 dollars
# 
# As seen from the above plot that the busisest location 237-236 has lower duration as compared other busisest location.
# 
# On the other hand 264-264 has higher duration and that could be the reason for the higher fare_amount.
# 
# It is observed that ,it is not at all necessary that the busiest route has higher other features as well. and for the business prospect we have to see the other routes as well for higher revenue genrations. One such route is 264-264.

# # Yellow Taxi June data

# ## Data Importing and Data Summarisation

# In[ ]:


# read file
trip_data = pd.read_csv('/content/drive/MyDrive/Data/yellow_tripdata_2020-06.csv')
trip_data.head()


# In[ ]:


trip_data.shape


# In[ ]:


trip_data.info()


# ## Data Cleaning and Manipulation Steps

# In[ ]:


# Droping unwanted column
trip_data.drop(['Unnamed: 0','VendorID','RatecodeID','store_and_fwd_flag','airport_fee','congestion_surcharge',],axis = 1, inplace =True)


# In[ ]:


# changing the datatype of datetime object
trip_data['tpep_pickup_datetime'] = pd.to_datetime(trip_data['tpep_pickup_datetime'])
trip_data['tpep_dropoff_datetime'] = pd.to_datetime(trip_data['tpep_dropoff_datetime'])


# In[ ]:


trip_data.info()


# In[ ]:


#droping nan values from data
trip_data.dropna(inplace = True)

#converting datatype of passenger count to int because float does not make any sense
trip_data['passenger_count'] = trip_data['passenger_count'].astype(int)


# In[ ]:


# create 'duration' column using pd.Timedelta(minutes=1)
trip_data['duration'] = (trip_data['tpep_dropoff_datetime'] - trip_data['tpep_pickup_datetime'])/ pd.Timedelta(minutes=1)
# create 'trip_pickup_hour' column using 'tpep_pickup_datetime' column
trip_data['trip_pickup_hour'] = trip_data['tpep_pickup_datetime'].dt.hour
# create 'trip_dropoff_hour' column using 'tpep_dropoff_datetime' column
trip_data['trip_dropoff_hour'] = trip_data['tpep_dropoff_datetime'].dt.hour
# create 'trip_day' column using 'tpep_pickup_datetime' column - use day_name()
trip_data['trip_day'] = trip_data['tpep_pickup_datetime'].dt.day_name()
# print data info
print(trip_data.info())
# print data head
trip_data.head()


# Now our Total_amount is basically Total_amount = fare_amount + tolls_amount + tip_amount + (extra + mta_tax + improvement_surcharge)
# 
# of the above components of total_amount we will specifically focus on 'fare_amount','tip_amount', 'tolls_amount' and 'total taxes'

# In[ ]:


# create 'total_taxes' column from summing 'extra','mta_tax', 'improvement_surcharge'
trip_data['total_taxes'] = trip_data['extra']+trip_data['mta_tax']+trip_data['improvement_surcharge']
# drop 'extra','mta_tax','improvement_surcharge' columns
trip_data.drop(['extra','mta_tax','improvement_surcharge'],axis=1,inplace=True)
# print data head
trip_data.head()


# For payment_type we have the following mapping for categories: 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip
# 
# let's just check if we have only these categories available in payment_type or not

# In[ ]:


# value_counts for 'payment_type' column
trip_data['payment_type'].value_counts()


# In[ ]:


# function for mapping numerical payment_type to actual payment
def map_payment_type(x):
    if x==1:
        return 'Credit_card'
    elif x==2:
        return 'Cash'
    elif x==3:
        return 'No_charge'
    elif x==4:
        return 'Dispute'
    elif x==5:
        return 'Unknown'
    else:
        return 'Voided_trip'

# use .apply and lambda on payment_type column to change 'payment_type' column
trip_data['payment_type'] = trip_data.payment_type.apply(lambda x:map_payment_type(x))
# print data head
trip_data.head()


# In[ ]:


trip_data.to_csv('/content/drive/MyDrive/Data/yellow_tripdata_2020-06_cleaned.csv')


# ## Data Analysis and Visualisation

# In[ ]:


trip_data


# ### Univariat Analysis

# In[ ]:


# continuous_columns list
continuous_columns = ['fare_amount','tip_amount','total_taxes','total_amount','duration','trip_distance','tolls_amount']


# In[ ]:


trip_data[continuous_columns].head()


# In[ ]:


# use .describe() for showing the statistics for continuous columns
trip_data[continuous_columns].describe()


# Since we are trying to understand the distribution of continuous numerical variables, we will be using
# 
# histograms box plots Below we have used a for loop to loop through all the continuous variables and then draw histograms and box plots for each of them at each iteration

# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# Negtive values for columns does not make sense fare_amount tip_amount total_taxes tolls_amount total_amount duration
# 
# Let's just observe how the negative values in each of these columns look like

# In[ ]:


# using .loc to show negative values in fare_amount  # 8 mil rows
trip_data.loc[trip_data['fare_amount']<0]


# In[ ]:


# using .loc to show negative values in tip_amount
trip_data.loc[trip_data['tip_amount']<0]


# In[ ]:


# using .loc to show negative values in tolls_amount
trip_data.loc[trip_data['tolls_amount']<0]


# In[ ]:


# using .loc to show negative values in total_taxes
trip_data.loc[trip_data['total_taxes']<0]


# In[ ]:


# using .loc to show negative values in total_amount
trip_data.loc[trip_data['total_amount']<0]


# In[ ]:


# data shape before filtering negative fare_amount rows
print(trip_data.shape)
# using .loc to filter only those rows where fare_amount is positive 
trip_data = trip_data.loc[trip_data['fare_amount']>=0]
# print data shape
print(trip_data.shape)
# print data.head()
trip_data.head()


# In[ ]:


print(trip_data.loc[trip_data['tip_amount']<0].shape)
print(trip_data.loc[trip_data['total_taxes']<0].shape)
print(trip_data.loc[trip_data['tolls_amount']<0].shape)


# In[ ]:


# using .loc to show negative values in duration
trip_data.loc[trip_data['duration']<0]


# In[ ]:


# using .loc to filter only those rows where duration is positive 
trip_data = trip_data.loc[trip_data['duration']>=0]
print(trip_data.shape)


# Now we will again look at the distribution plots for these variables

# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# In[ ]:


# use .describe() again to show the statistics for these continuous variables
trip_data[continuous_columns].describe()


# In[ ]:


# for loop for continuous_columns variable
for feature in continuous_columns:
    # removing the outliers
    feature_data_percentile = trip_data[feature].quantile(0.95)
    feature_data = trip_data.loc[trip_data[feature]<feature_data_percentile,feature]
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(feature_data)
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(feature_data,ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()


# Looking from the above histograms and box plots we can decipher following information for each column
# 
# fare_amount - most of the fare amount is within 8.5 dollar value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 940 dollars.
# 
# tip_amount - most of the tip amount is within 1.5 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 400 dollars.
# 
# tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.
# 
# total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. There is very less outliers.
# 
# total_amount - most of the total_amount values is within 14 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.some Heavy outlier exist of 1100 dollar
# 
# duration - most of the values in duration is within 8.86 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 4000 minutes.
# 
# trip_distance - most of the trip_distance is within 1.7 miles value as is shown by the median. only a heavy outliers exit of around 22k miles.

# categorical_variables

# In[ ]:


# list of categorical_variables
categorical_variables = ['payment_type','trip_pickup_hour','trip_dropoff_hour','trip_day','PULocationID','DOLocationID']


# In[ ]:


# start exploration with payment_type using .value_counts()
trip_data['payment_type'].value_counts()


# In[ ]:


# but this is a series for ease of plotting we need to use dataframe using .reset_index() on value_counts()
payment_type_category_count = trip_data['payment_type'].value_counts().reset_index()
# print the above dataframe
payment_type_category_count


# In[ ]:


# we are shown the count under each category but it is better to have count% for comparison - create count_percent col
payment_type_category_count['count_percent'] = (payment_type_category_count['payment_type']/trip_data.shape[0])*100
# print the data frame
payment_type_category_count


# In[ ]:


# now let's plot it as bar chart
# first step - create fig, ax object using plt.subplots
fig,ax = plt.subplots(figsize=(7,7))
# second step - use sns.barplot(x, y , data, ax) for plotting bar plot
sns.barplot(x = 'index', y = 'count_percent', data=payment_type_category_count,ax=ax)
# third step - use ax object to change plot properties - here we set a title with ax.set_title()
ax.set_title('box plot for payment_type column')
# third step - seaborn style setting
sns.set()
# fourth step - use plt.show() for showing the plots
plt.show()


# From above we can understand that most of the payments are done through cash and credit cards. The proportion of credit card payments is around 70%.
# 
# Now we look into time based categorical variables.
# 
# 'trip_pickup_hour' 'trip_dropoff_hour' 'trip_day'

# In[ ]:


# now let's plot all the time based categorical variables in this way using a for loop
for feature in ['trip_pickup_hour','trip_dropoff_hour','trip_day']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    if feature_value_counts.shape[0]<10:
        fig,ax = plt.subplots(figsize=(7,7))
    else:
        fig,ax = plt.subplots(figsize=(20,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# Based on above plots we can observe following things
# 
# Trip Hour 1) The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 9 min.
# 
# 2) Peak hour for the pick up and drop off is around evening from 13 to 16. The busiest time is 15 PM.
# 
# 3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.
# 
# Trip day
# 
# 1)Sunday has the lowest taxi uses while Tuesday is the busiest.
# 
# 2)Weekdays have heavy taxi uses compared to the weekands
# 
# Moving on we will explore the distribution of location based features:
# 
# 'PULocationID'
# 
# 'DOLocationID'

# In[ ]:


# let's see the number of categories available in both pickup and dropoff location - PULocationID and DOLocationID
print(trip_data['PULocationID'].value_counts().shape)
print(trip_data['DOLocationID'].value_counts().shape)


# In[ ]:


for feature in ['PULocationID','DOLocationID']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    fig,ax = plt.subplots(figsize=(25,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# The above plots looks quite messy but one insight that we can indetify from above plot that most of pickup and dropoff points do not have more 0.5% traffic (0.5 percent of 8755612 total trips is 43778).
# 
# So in our next plot we will filter out these pickup and dropoff points to look into the graph more clearly.

# In[ ]:


for feature in ['PULocationID','DOLocationID']:
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # filter only those location which has more than 0.5 % of traffic
    feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.5]
    print('Number of categories in feature '+ feature + ' above 0.5 % count is ' + str(feature_value_counts.shape[0]))
    fig,ax = plt.subplots(figsize=(25,7))
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    ax.set_title('Bar plot for '+ feature)
    ax.set_xlabel(feature)
    sns.set()
    plt.show()


# From the above plots we can glance following insights
# 
# The busiest location in terms of pickup are 236 and 237
# 
# The busiest location for dropoff too are 236 , 237 and 79 busiest locations but 236 is far more busiest than the other two in drop_off hour.
# 
# For exploring busy routes we need to create a new route column which is a combination of pickup and dropoff point.
# 
# So route = 'PULocationID'-'DULocationID'

# In[ ]:


# create routes column using PULocationID and DOLocationID with lambda function
trip_data['routes'] = trip_data.apply(lambda x: str(x['PULocationID'])+'-'+str(x['DOLocationID']),axis=1)


# In[ ]:


trip_data['routes'].head()


# In[ ]:


# plot bar plot for routes which have trip count above 0.25%
feature = 'routes'
feature_value_counts = trip_data[feature].value_counts().reset_index()
feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
# choosing routes where the trip percent is above 0.25% of total trips
feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.25]
print('Number of categories in feature '+ feature + ' above 0.25 % count is ' + str(feature_value_counts.shape[0]))
fig,ax = plt.subplots(figsize=(25,7))
sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
ax.set_title('Bar plot for '+ feature)
ax.set_xlabel(feature)
sns.set()
plt.show()


# From the above plot we can observe that 5 busiest route are following:
# 
# 264-264
# 
# 237-236
# 
# 236-237
# 
# 236-236

# In[ ]:


# look into value_counts of 'passenger_count'
trip_data['passenger_count'].value_counts()


# Here we see that the mostly 1 or 2 passengers avail the cab. The instance of large group of people travelling together is rare

# ### Bivariate Analysis

# PRICING VARIABLE EXPLORATION WITH HOUR/DAY OF TRIP *
# 
# All of our pricing variables are continuous and Hour/Day is categorical.
# 
# The way to explore relationship between a continuous variable and categorical variable is through a box plot. We create box plot for each category of categorical variable.
# 
# so as to see how the distribution changes for the continuous variables as the category values changes for categorical variable.
# 
# We will start with fare_amount exploration.

# In[ ]:


# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()


# In[ ]:


# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()


# From the above plot we can observe that most of the outliers in fare_amount happens during 10AM to 7PM based on pickup time.
# 
# From the above plot trip_dropoff_hour outliers happens during 14 or 2PM to 20 or 8PM based on pickup time.
# 
# Outliers is less in the late nights and early morning.
# 
# For observing the distribution in a better way we would restrict the fare_amount to below 50 dollars.

# In[ ]:


# restricted_fare_amount_data dataframe formation by filtering fare_amount less than 50 dollars
restricted_fare_amount_data = trip_data.loc[(trip_data['fare_amount']<=50) & (trip_data['fare_amount']>=0)]
restricted_fare_amount_data.shape


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()


# We can obseve from the above graph the fare_amount in late nigth is comparitively higher than the rest of the hours(same pattern seen in both the cases).
# 
# Also the median fare_amount between 5 - 6 is less than all others hours of the day(seen in bothe cases)
# 
# let's us see if hour of day has any effect on other pricing related variables or not.
# 
# Starting with total_amount

# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
# sns.boxplot changes
sns.boxplot(x = 'trip_pickup_hour',y='total_amount',data=trip_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
# sns.boxplot changes
sns.boxplot(x = 'trip_dropoff_hour',y='total_amount',data=trip_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


# restricted_total_amount_data for filtering total_amount data to less than 50 dollars
restricted_total_amount_data = trip_data.loc[trip_data['total_amount']<=50]
restricted_total_amount_data.shape


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()


# the pattern of total_amount is same as the pattern we seen in the fare_amount

# In[ ]:


restricted_tip_amount_data = trip_data.loc[trip_data['tip_amount']<10]
restricted_total_taxes_data = trip_data.loc[trip_data['total_taxes']<10]


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()


# The median of tip_amount in early morning is mostly zero but IQR is high that means the some of the tip amounts are higher end).
# 
# And in between 11 -14 the tip_amount is minimum and almost constant, whereas tip amount is on higher side in evenings.
# 
# (Same pattern seen in both the trip_pickup and trip_drop_off)

# In[ ]:


# total_taxes = extra + improvement_surcharges + Mta

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()


# The taxs imposed from 16 to 19 is much higher as compared to the other hours beacue traffic surcharge.
# 
# The taxes in the period between 6 to 15 is much lower than the other pick_up hours

# In[ ]:


# plot of trip_day with fare_amount
fig,ax = plt.subplots(figsize=(7,7))
# changes in sns.boxplot x and y
sns.boxplot(x = 'trip_day',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt the day of the week')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt the day of the week')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt the day of the week')
sns.set()
plt.show()


# In[ ]:


fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt the day of the week')
sns.set()
plt.show()


# We can see that pricing overall does not change much with respect to day of week.but total taxes are higher in weekdays compared to weekands

# In[ ]:


# create a new series using value_counts() on 'PULocationID'
pickup_location_value_counts = trip_data['PULocationID'].value_counts()
# show the series
pickup_location_value_counts.head()


# In[ ]:


# top 10 frequent pickup locations using .nlargest(10).index
top_10_frequent_pickup_locations = pickup_location_value_counts.nlargest(10).index
top_10_frequent_pickup_locations


# In[ ]:


# for loop for plotting box plot of each of the top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median fare_amount for the top_pickup_locID
    print('The median fare_amount of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['fare_amount'].median()))
    # fig,ax object
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of fare_amount from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()


# So from above plot we can observe that for one of the most busiest pickup location i.e 236 has median fare_amount is low in comparison to other busiset location.
# 
# It is also observe that the median fare_amount is highest for the location ID 140 which is about 9.5 dollars
# 
# This could be helpful in adjusting our revenue expectation based on putting our cabs in a given location because just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.

# ### Duration Exploration

# In[ ]:


# plot box plot for duration for different hours of day
fig,ax = plt.subplots(figsize=(20,7))
# box plot using sns.boxplot x is 'trip_pickup_hour' and y is 'duration'
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = trip_data,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()


# In[ ]:


# create restricted_duration dataframe with .loc on 'duration' column
restricted_duration= trip_data.loc[trip_data['duration']<50]
restricted_duration.shape


# In[ ]:


fig,ax = plt.subplots(figsize=(20,7))
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = restricted_duration,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()


# The duration of trip is higher in the early morning and late nights whereas in pickup_hour 5-7 AM the duration of trip is lowest.

# In[ ]:


# plot box plots of duration for top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median duration for the top_pickup_locID
    print('The median trip duration of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['duration'].median()))
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()


# As seen from the above plot the busiset location not has the longest duration of trip, but the other busiset location that is 140 has higher duration (thats why that location has higher fare_amount too)

# ### Analyse Routes

# We could analyse routes with fare_amount or total_taxes and duration for different time of the day.

# In[ ]:


# counting the routes of the trip_data
trip_route_value_counts = trip_data['routes'].value_counts()


# In[ ]:


trip_route_value_counts.head(10)


# In[ ]:


# 10 busiest routes in trip_data
trip_route_top_10 = trip_route_value_counts.nlargest(10).index


# In[ ]:


trip_route_top_10


# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median fare_amount for the respective route
    print("the fare amount for the route " + trip_route +' '+ 'is ' + str(trip_route_df['fare_amount'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()


# From above plot it is clear that the busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is lower than the other Busiset trip_routes.
# 
# the trip_route 264-264 has the highest fare_amount of 8.5 median.Its worthnoting that these route should be kept in mind for business prospect.

# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the fare amount for the route " + trip_route +' '+ 'is ' + str(trip_route_df['total_taxes'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['total_taxes'],ax=ax)
    # set_title
    ax.set_title('box plot of total_taxes for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()


# From the above plot it is clearly vissible almost all routes has same total_tax of 1.3 and 1.8 dollars, but the trip_route 264-264 and 75-74 lowest total_tax i.e 0.8 dollars as well.
# 
# As we seen from fare_amount plot of routes, the 264-264 route has higher fare amount as compared to other routes but it could be higher because of lower taxes applied on the these route as shown in above plot. as it has lowest total_tax value of 0.8 dollars

# In[ ]:


for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the duration for the route " + trip_route +' '+ 'is ' + str(trip_route_df['duration'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe  trip_route_df 
    sns.boxplot(trip_route_df['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for trip_route '+ trip_route)
    sns.set()
    plt.show()


# As seen from the above plot that the busisest location 264-264 has 6.96, highest duration as compared other busisest location.

# ## Final Results from EDA

# fare_amount - most of the fare amount is within 8.5 dollar value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 940 dollars.
# 
# tip_amount - most of the tip amount is within 1.5 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 400 dollars.
# 
# tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.
# 
# total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. There is very less outliers.
# 
# total_amount - most of the total_amount values is within 14 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.some Heavy outlier exist of 1100 dollar
# 
# duration - most of the values in duration is within 8.86 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 4000 minutes.
# 
# trip_distance - most of the trip_distance is within 1.7 miles value as is shown by the median. only a heavy outliers exit of around 22k miles.
# 
# most of the payments are done through cash and credit cards. The proportion of credit card payments is around 70%.
# 
# Trip Hour
# 
# 1) The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 9 min.
# 
# 2) Peak hour for the pick up and drop off is around evening from 13 to 16. The busiest time is 15 PM.
# 
# 3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.
# 
# Trip day
# 
# 1)Sunday has the lowest taxi uses while Tuesday is the busiest.
# 
# 2)Weekdays have heavy taxi uses compared to the weekands
# 
# location_ID-The busiest location in terms of pickup are 236 and 237
# 
# The busiest location for dropoff too are 236 , 237 and 79 busiest locations but 236 is far more busiest than the other two in drop_off hour.
# 
# The mostly 1 or 2 passengers avail the cab. The instance of large group of people travelling together is rare.
# 
# The fare_amount in late nigth is comparitively higher than the rest of the hours(same pattern seen in both the cases).
# 
# Also the median fare_amount between 5 - 6 is less than all others hours of the day(seen in bothe cases)
# 
# The median of tip_amount in early morning is mostly zero.And in between 11 -14 the tip_amount is minimum and almost constant, whereas tip amount is on higher side in evenings.
# 
# The taxs imposed from 16 to 19 is much higher as compared to the other hours beacue traffic surcharge.
# 
# The taxes in the period between 6 to 15 is much lower than the other pick_up hours
# 
# Pricing overall does not change much with respect to day of week.But total taxes are higher in weekdays compared to weekands
# 
# For one of the most busiest pickup location i.e 236 has median fare_amount is low in comparison to other busiset location.
# 
# It is also observe that the median fare_amount is highest for the location ID 140 which is about 9.5 dollars
# 
# This could be helpful in adjusting our revenue expectation based on putting our cabs in a given location because just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.
# 
# The duration of trip is higher in the early morning and late nights whereas in pickup_hour 5-7 AM the duration of trip is lowest.
# 
# The busiset location not has the longest duration of trip, but the other busiset location that is 140 has higher duration (thats why that location has higher fare_amount too)
# 
# The busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is lower than the other Busiset trip_routes.
# 
# The trip_route 264-264 has the highest fare_amount of 8.5 median.Its worthnoting that these route should be kept in mind for business prospect.
# 
# Almost all routes has same total_tax of 1.3 and 1.8 dollars, but the trip_route 264-264 and 75-74 lowest total_tax i.e 0.8 dollars as well.
# 
# As we seen from fare_amount plot of routes, the 264-264 route has higher fare amount as compared to other routes but it could be higher because of lower taxes applied on the these route as shown in above plot. as it has lowest total_tax value of 0.8 dollars
# 
# The busisest location 264-264 has 6.96, highest duration as compared other busisest location.

# # Final Output

# •	Foremost important thing that was obtained from data, the number of trips in post-pandemic period (June 2022) is greatly reduced around 93% as compared to in pre-pandemic period (February 2022).
# 
# •	Fare amount decreases little bit after pandemic i.e., 9 to around 8.5, but there is a significant change in maximum amount it will reach around 940 dollars which is around 6000 dollars in pre-pandemic period.
# 
# •	Tip amount also decreases from 2 dollars to 1.5 dollars.
# 
# •	Toll amount not significant change between periods.
# 
# •	Total Taxes: There is no change in total taxes.
# 
# •	Duration of the trip decreased from around 12 min to 8.6 min after the pandemic period. 
# 
# •	Trip Distance: There is not such a significant change in trip distance.
# 
# •	Payment type: Credit card will be more preferred for payment followed by cash in both periods.
# 
# •	Trip Pickup / Trip Dropoff: For trip pick up the peak hours in pre-pandemic is in evening from 5PM to 7PM and busiest time was 6PM, but in post-pandemic it will be around 1PM to 4PM with busiest time was 3PM. The drop off time for trip is almost same as pick up hours in both periods.
# 
# •	Trip Day: Tuesday is the day on which there are a greater number of trips occurred while Sunday with a smaller number of trips done in pre-pandemic period. But in post-pandemic period Saturday is the busiest day with most number while Sunday with smaller number of trips occurred.
# 
# •	Location: The busiest location for pickup and drop off 161 ,237 and 236 in pre-pandemic period, while in post-pandemic it will be 236 and 237.
# 
# •	Mostly 1 or 2 passengers avail the cab in both periods.
# 
# •	Busiest routes are 237-236 and 236-236 in pre-pandemic and in post-pandemic it will be 264-264 and 237-236.
# 
# •	In pre-pandemic period the fare amount almost constant throughout pickup hours, but in post-pandemic in late night trips the fare amount more as trips occurred in day pickup hours.
# 
# •	The tip amount is less in the morning period and almost constant for remaining period in pre-pandemic while it is more in evening and almost 0 in late night trips in post-pandemic.
# 
# •	Total taxes are almost same in both periods. The variation in total taxes is higher in early morning in pre-pandemic but after pandemic the variation in early morning are negligible.
# 
# •	Total taxes are more in weekdays in post-pandemic but not much significant change in pre-pandemic.
# 
# •	The median fare amount was highest in location id 186 in pre-pandemic, in post-pandemic the fare amount is highest for location id 140 (it was seen in the 10 busiest locations and it’s worth noting that both of above id’s are not busiest one hence we can conclude that busiest location doesn’t assure you higher revenue generation.) (These are those 2 locations where duration of trip is also high)
# 
# •	As far as routes are concerned the route 161-237 has higher median fare amount in pre pandemic, whereas in post pandemic route 264-264 has highest fare amount. (it was seen in the 10 busiest route and it’s worth noting that both of above id’s are not busiest one hence we can conclude that busiest route doesn’t assure you higher revenue generation.) (These are those 2 routes where duration of trip is also high)
# 
# 
# 
# 
