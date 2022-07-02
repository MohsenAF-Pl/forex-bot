# this was for a project of mine and is not related to this project
import requests
from datetime import datetime
import pandas as pd

"""
pair = 'EURUSD'
start_date = '2021-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
api_key = 'Zqk5McQKLRxIrF97Hi1be6kf_3A0fEdA'

url = f'https://api.polygon.io/v2/aggs/ticker/C:{pair}/range/1/day/{start_date}/{end_date}?apiKey={api_key}'

data = requests.get(url).json()
df = pd.DataFrame.from_dict(data)
df.to_pickle('eurusd.pkl')
"""

data = pd.read_pickle('eurusd.pkl')
print(data.results[2]['c'])