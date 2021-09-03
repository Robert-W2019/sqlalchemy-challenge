#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[ ]:





# In[2]:


import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[25]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


# In[26]:


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
inspector = inspect(engine)


# In[27]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[28]:


# View all of the classes that automap found
Base.classes.keys()


# In[29]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[30]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Precipitation Analysis

# In[31]:


measurement_columns = inspector.get_columns('Measurement')
for columns in measurement_columns: 
    print(columns["name"], columns["type"])


# In[37]:


# Find the most recent date in the data set.
first_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()


last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

print(f"First date {first_date} Last date {last_date}")


# In[43]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 

# Calculate the date one year from the last date in data set.
prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame (results, columns=['date', 'precipitation'])
df.set_index(df['date'], inplace=True)

# Sort the dataframe by date
df = df.sort_index()

# Use Pandas Plotting with Matplotlib to plot the data
df.plot(rot=90)


# In[44]:


# Use Pandas to calcualte the summary statistics for the precipitation data
df.describe()


# # Exploratory Station Analysis

# In[45]:


# Design a query to calculate the total number stations in the dataset
session.query(func.count(Station.station)).all()


# In[47]:


# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


# In[48]:


# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).    filter(Measurement.station == 'USC00519281').all()


# In[50]:


# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

from pandas.plotting import table
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

results = session.query(Measurement.tobs).    filter(Measurement.station == 'USC00519281').    filter(Measurement.date >= prev_year).all()
df = pd.DataFrame(results, columns=['tobs'])
df.plot.hist(bins=12)

plt.tight_layout


# # Close session

# In[51]:


# Close Session
session.close()


# In[ ]:




