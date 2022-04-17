# helpful: prometheus.io/docs/prometheus/latest/querying/api/
from requests import get
import json
from tkinter import *

data = get('http://localhost:9090/api/v1/query', params={'query': 'temperature_data'})
data = data.json()
# data = json.loads(data)
print(data['data']['result'][0]['value'])
