# Name:     run_get_bls_data.py
# Date:     2025-06-20
# Author:   STEVEN M. GURIDI
#
# Description:
# Use the c_bls_data class to obtain series of data
# from the US Bureau of Labor Statistics (BLS) API.
import csv
import numpy as np
import pandas as pd
from paths import DATA_DIR, SECRETS_DIR
from CPI_Puller import CPI_Puller
from Power_Delivery import Power_Delivery
from US_Labor_Force import US_Labor_Force
from Lumber import US_Lumber

# @params API Key, Export_File, Series ID, start year, and year
df_ky = pd.read_csv(SECRETS_DIR / 'API_KEY.csv')
BLS_API_KEY = df_ky['BLS_API'][0]
#OUTPUT DEFLATOR ID: IPUCN2211__T051000000, REAL SECTOR OUTPUT ID: IPUCN2211__T011000000
Power_Delivery = Power_Delivery(BLS_API_KEY, DATA_DIR / 'POWER_OUTPUT_2007-Current.csv'
                                ,['IPUCN2211__T051000000', 'IPUCN2211__T011000000']
                                , 2007, 2025 )

Lumber = US_Lumber(BLS_API_KEY, DATA_DIR / 'LUMBER_HOUSES_2007-Current.csv',
                ['PCU321991321991'], 2007, 2025)