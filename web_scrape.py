import json
import requests
import re 
fin_data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo")
#print(fin_data)
source = fin_data.json()
print(type(source))
#print(source.keys())
#print(source['Meta Data'])
for k, v in source['Time Series (Daily)'].items():
    #print(f"Key: {k}")
    #print(f"{v}")
    if re.search("\d+[.]\d+" , str(v)):
        print(v)
    else:
        break
    


