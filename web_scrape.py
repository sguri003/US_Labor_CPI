import json
import requests

fin_data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo")
print(fin_data)
source = fin_data.text
data = json.loads(source)
print(data)