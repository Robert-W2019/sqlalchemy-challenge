# sqlalchemy-challenge

```python
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
```


```python

```


```python
import numpy as np
import pandas as pd
import datetime as dt
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
```


```python
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
inspector = inspect(engine)
```


```python
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
```


```python
# View all of the classes that automap found
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

```


```python
# Create our session (link) from Python to the DB
session = Session(engine)
```

# Exploratory Precipitation Analysis


```python
measurement_columns = inspector.get_columns('Measurement')
for columns in measurement_columns: 
    print(columns["name"], columns["type"])
```

    id INTEGER
    station TEXT
    date TEXT
    prcp FLOAT
    tobs FLOAT
    


```python
# Find the most recent date in the data set.
first_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()


last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

print(f"First date {first_date} Last date {last_date}")

```

    First date ('2010-01-01',) Last date ('2017-08-23',)
    


```python
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


```



![png](https://github.com/Robert-W2019/sqlalchemy-challenge/blob/main/Output/output_13_1.png?raw=true)
    



```python
# Use Pandas to calcualte the summary statistics for the precipitation data
df.describe()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2021.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.177279</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.461190</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.130000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.700000</td>
    </tr>
  </tbody>
</table>
</div>



# Exploratory Station Analysis


```python
# Design a query to calculate the total number stations in the dataset
session.query(func.count(Station.station)).all()
```




    [(9,)]




```python
# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
```




    [('USC00519281', 2772),
     ('USC00519397', 2724),
     ('USC00513117', 2709),
     ('USC00519523', 2669),
     ('USC00516128', 2612),
     ('USC00514830', 2202),
     ('USC00511918', 1979),
     ('USC00517948', 1372),
     ('USC00518838', 511)]




```python
# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()


```




    [(54.0, 85.0, 71.66378066378067)]




```python
# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

from pandas.plotting import table
prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
df = pd.DataFrame(results, columns=['tobs'])
df.plot.hist(bins=12)

plt.tight_layout


```



    
![png](https://github.com/Robert-W2019/sqlalchemy-challenge/blob/main/Output/output_19_1.png?raw=true)
    


# Close session


```python
# Close Session
session.close()
```


```python

```