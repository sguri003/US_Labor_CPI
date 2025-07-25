import csv
import pandas as pd         
import numpy as np  
#altering  dd
df_ky = pd.read_csv('API_KEY.csv')
print(df_ky['BLS_API'][0])
print(type(df_ky))
print(dict(df_ky).items)
dc = dict(df_ky)
df_api = pd.DataFrame(df_ky)
print(df_api)
