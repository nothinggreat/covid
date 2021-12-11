import pandas as pd
import numpy.ma as ma
import io
import requests
import matplotlib.pyplot as plt
OUTLIER_COUNT = 1000

url="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
content=requests.get(url).content
df=pd.read_csv(io.StringIO(content.decode('utf-8')))

hudson = df[df['county'] == "Hudson"].copy()
hudson['prior_cases'] = hudson['cases'].shift(1)
hudson['prior_cases'] = hudson['prior_cases'].fillna(0).astype(int)
hudson['new_cases'] = hudson['cases'] - hudson['prior_cases']
mask = (hudson['new_cases'] > OUTLIER_COUNT) | (hudson['new_cases'] < 0)

latest_cases = hudson['new_cases'].iloc[-1]
latest_date = hudson['date'].iloc[-1]

dates=pd.to_datetime(hudson['date'],format="%Y-%m-%d")
masked_cases=ma.masked_array(hudson['new_cases'],mask=mask)

plt.plot(dates,masked_cases)
plt.title("Through " + str(latest_date))
plt.xlabel('Date')
plt.ylabel('New Cases')
#plt.show()
plt.savefig('C:/Users/Daniel/Desktop/' + str(latest_cases) + '_New_Cases.png')
plt.close()
