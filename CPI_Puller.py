# DATA: 2025-06-21
# NOTES: Retrieving Data from BLS to understand key labor sectors. 
# To use this LABOR_US class, each use must provide their own BLS API Version 2
# registration key from here: https://data.bls.gov/registrationEngine/

#NOTE: OPEN SOURCE PROJECT @https://github.com/sguri003/Labor_Stats_Dev

# To use the c_bls_data class, create an instance with below parameter in constructor:
import os 
import json
import csv
import requests
import numpy as np                
import pandas as pd                   
#new comming
class CPI_Puller:
    #CONSTRUCTOR APsI KEY, OUTPUT FILE, START AND END YEAR
    def __init__(self, reg_key, out_file_nm, series_id, start_year, end_year):        # Set the file name variable and create the parameters for the API request.
        #instance variables of CPI_Puller classs
        self.out_file_nm = out_file_nm
        headers = {'Content-type': 'application/json'}
        parameters = json.dumps({'seriesid' : series_id, 'startyear' : start_year, 'endyear' : end_year, 'calculations' : True , 'registrationkey' : reg_key})
        # Get data in JSON format and then write it to a CSV file.
        json_data = self.get_cpi(headers, parameters)
        self.data_to_csv(json_data)
        
        
    #retrive cpi data from BLS AP
    def get_cpi(self, headers, parameters):
        #Fire Post to end point BLS Grab Json
        post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data = parameters, headers = headers)
        json_data = json.loads(post.text)
        return json_data

    def data_to_csv(self, json_data):
        # Convert the data from JSON format to CSV records. Write
        # each record to the specified output file.
        if os.path.exists(self.out_file_nm):
            os.remove(self.out_file_nm)
            print(f"File '{self.out_file_nm}' deleted successfully.")
        else:
            print(f"File '{self.out_file_nm}' does not exist.")    
        #open file to be written to CSV. 
        with open(self.out_file_nm, mode = 'w', newline = '') as data_file:
            #Series ID is category such as Gasoline, Groceries. 
            fieldnames = ['Series ID', 'Date', 'Value', 'Annual Percent Change']
            d_wrtr = csv.writer(data_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            #Place Headers
            d_wrtr.writerow(fieldnames)
            # Write each record to the output file.
            for series in json_data['Results']['series']:
                series_id = series['seriesID']
                for item in series['data']:
                    # Get the basic data
                    year = item['year']
                    period_name = item['periodName']
                    value = item['value']
                    # Get the 12-month change
                    calculations = item['calculations']
                    pct_changes = calculations['pct_changes']
                    annual_pct_chg = pct_changes['12']
                    # Create a month field in the format of a date for 
                    # the first day of each month (for example: January 1, 2022).
                    month = period_name + ' 1 ' + year
                    #Write the CSV record to the output file.
                    d_wrtr.writerow([series_id, month, value, annual_pct_chg])
        #place in dataframe format from
        dt = pd.read_csv(self.out_file_nm)
        df_cpi = pd.DataFrame(data=dt)
        df_cpi['Date'] = pd.to_datetime(dt['Date'], format="mixed")
        df_cpi.to_csv("CPI_2010_Current_Frame.csv")
        print(df_cpi)