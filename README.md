QInfluxDB
=========

A little ORM for [InfluxDB](https://github.com/influxdb/influxdb) based on the
[python wrapper for InfluxDB](https://github.com/influxdb/influxdb-python).

Installation
------------

```
pip install git+https://github.com/unaizalakain/qinfluxdb.git
```


Example use case
----------------

```
from qinfluxdb import Client

# The client is just a wrapper around InfluxDB's python client
client = Client(database='analytics', timeout=60)

query = client.q.from_series('temperature')

# Iterate over the results
for result in query:
    print(result)

# List them all
query.all()

# Continue with the query and filter
query.where('value > 20').limit(20)

# Only select some of the values
query.values('time', 'mean(value)').group_by('time(1d)')

# Advanced filters
from qinfluxdb import Q

hot = Q('value > 30')
cold = Q('value < 0')
extreme = hot | cold
query.where(extreme)
```

**More coming!**
