# Name:     main_eia.py
# Description:
# Use the EIA_Electricity class to pull the past 10 years of US
# electricity price, usage, and output from the EIA API.
import pandas as pd
from EIA_Electricity import EIA_Electricity
from Database import Database

df_ky = pd.read_csv('API_KEY.csv')
EIA_API_KEY = df_ky['EIA_KEY'][0]

Electricity = EIA_Electricity(EIA_API_KEY, 'Electricity_10yr.csv')

# load into SQL Server so downstream work reads from the DB instead of
# re-pulling from the EIA API every time
db = Database()
db.write_df(pd.read_csv('Electricity_10yr.csv'), 'Electricity_Monthly')
db.close_cnx()
