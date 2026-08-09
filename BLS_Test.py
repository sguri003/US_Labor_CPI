import os 
import json
import csv
import requests
import numpy as np                
import pandas as pd  

class BLS_Test:
    #CONSTRUCTOR APsI KEY, OUTPUT FILE, START AND END YEAR
        def __init__(self, reg_key, out_file_nm, series_id, start_year, end_year):        # Set the file name variable and create the parameters for the API request.
            #instance variables of CPI_Puller classs
            self.out_file_nm = out_file_nm
            headers = {'Content-type': 'application/json'}
            parameters = json.dumps({'seriesid' : series_id, 'startyear' : start_year, 'endyear' : end_year, 'calculations' : True , 'registrationkey' : reg_key})
            # Get data in JSON format and then write it to a CSV file.
            json_data = self.get_cpi(headers, parameters)
        
        
    #retrive cpi data from BLS AP
        def get_cpi(self, headers, parameters):
            #Fire Post to end point BLS Grab Json
            post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data = parameters, headers = headers)
            json_data = json.loads(post.text)
            print("https://api.bls.gov/publicAPI/v2/timeseries/data/"+str(parameters) +  str(headers))
            with open('BLS_Test.json', 'w') as out_api:
                json.dump(json_data, out_api, indent=4)
            return json_data

df_ky = pd.read_csv('API_KEY.csv')
BLS_API_KEY = df_ky['BLS_API'][0]
print(BLS_Test)
BLS_Test = BLS_Test(BLS_API_KEY, 'BLS_Testing.csv'
                                ,['IPUCN2211__T051000000', 'IPUCN2211__T011000000']
                                , 2010, 2025 )

