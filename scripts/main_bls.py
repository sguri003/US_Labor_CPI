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
# CUSR0000SA0 - All items in U.S. city average, all urban consumers, seasonally adjusted
# CUSR0000SETB01 - Gasoline (all types) in U.S. city average, all urban consumers, seasonally adjusted
# CUSR0000SAF1 - Food in U.S. city average, all urban consumers, seasonally adjusted
# CUSR0000SETA02 - Used cars and trucks in U.S. city average, all urban consumers, seasonally adjusted
df_ky = pd.read_csv(SECRETS_DIR / 'API_KEY.csv')
BLS_API_KEY = df_ky['BLS_API'][0]
#OUTPUT DEFLATOR ID: IPUCN2211__T051000000, REAL SECTOR OUTPUT ID: IPUCN2211__T011000000
#bls_dt = labor_US(BLS_API_KEY, 'POWER DELIVER SG.CSV' , ['IPUCN2211__T051000000', 'IPUCN2211__T011000000'], 2000, 2022 )
#CPI for Gas, Groceries, necessities.
#CPI-->CUSR0000SA0 ALL URBAN AREAS
CPI_Data = CPI_Puller(BLS_API_KEY, DATA_DIR / 'CPI_2015-Testing.csv',
                        ['CUSR0000SA0','CUSR0000SETB01', 'CUSR0000SAF1', 'CUSR0000SETA02']
                        , 2010, 2025)
Power_Delivery = Power_Delivery(BLS_API_KEY, DATA_DIR / 'POWER_OUTPUT_2015-2025_Aug.csv'
                                ,['IPUCN2211__T051000000', 'IPUCN2211__T011000000']
                                , 2015, 2025 )
# Labor Civilian Workforce code: LNS11000000, Employment code: LNS12000000
# 16 years and older and under 65 years old all civilians
#Pay and Benefits NBU20530000000000033030
Labor = US_Labor_Force(BLS_API_KEY, DATA_DIR / 'Labor_Force_2015-2025_Aug.csv'
                                ,['LNS11000000','LNS12000000']
                                , 2015, 2025 )

Labor = US_Labor_Force(BLS_API_KEY, DATA_DIR / 'Employee_Data2015-2025_Aug.csv'
                                ,['CES0500000003',' CES0000000001', 'JTU110099000000000HIL']
                                , 2015, 2025 )
#PCU321991321991  Manufactured home, mobile home, manufacturing
Lumber = US_Lumber(BLS_API_KEY, DATA_DIR / 'LUMBER_HOUSES_2015-2025_Aug.csv',
                ['PCU321991321991'], 2015, 2025)
