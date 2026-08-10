# Name:     main_eia_fl.py
# Description:
# Use the EIA_Electricity class to pull the past 10 years of Florida
# electricity price, usage, and output from the EIA API.
import pandas as pd
from paths import DATA_DIR, SECRETS_DIR
from EIA_Electricity import EIA_Electricity
from Database import Database

df_ky = pd.read_csv(SECRETS_DIR / 'API_KEY.csv')
EIA_API_KEY = df_ky['EIA_KEY'][0]

out_file = DATA_DIR / 'Electricity_10yr_FL.csv'
Electricity = EIA_Electricity.for_florida(EIA_API_KEY, out_file)
Electricity.plot_price_only()

# load into SQL Server so downstream work reads from the DB instead of
# re-pulling from the EIA API every time
db = Database()
db.write_df(pd.read_csv(out_file), 'Electricity_Monthly_FL')
db.close_cnx()
