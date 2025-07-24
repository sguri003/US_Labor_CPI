#CIVILIAN LABOR FORCE DATA PULL
#LABOR FORCE CONSIST OF 16 YEARS OLD TO 65 YEARS OLD. 
#NOTE: OPEN SOURCE PROJECT @https://github.com/sguri003/Labor_Stats_Dev
# AUTHOR: @sguri003
# To use the c_bls_data class, create an instance with below parameter in constructor:
import os 
import json
import csv
import requests
import numpy as np    
import pandas as pd     
import matplotlib.pylab as plt
import re



class US_Labor_Force:
    #CONSTRUCTOR FOR POWER DELIVERY. 
    def __init__(self, reg_key, out_file_nm, series_id, start_year, end_year):        # Set the file name variable and create the parameters for the API request.
        #instance variables of CPI_Puller classs
        self.out_file_nm = out_file_nm
        headers = {'Content-type': 'application/json'}
        parameters = json.dumps({'seriesid' : series_id, 'startyear' : start_year, 'endyear' : end_year, 'calculations' : True , 'registrationkey' : reg_key})
        # Get data in JSON format and then write it to a CSV file.
        json_data = self.get_Labor(headers, parameters)
        #@param json data retrieve civilian labor force. 
        self.Labor_to_DF(json_data)
        
    def get_Labor(self, headers, parameters):
        #Fire Post to end point BLS Grab Json
        post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data = parameters, headers = headers)
        json_data = json.loads(post.text)
        return json_data
    
    #Pull Active Labor Force ages 16-65 years old
    #@param @self @json_data 
    def Labor_to_DF(self, json_data):
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
        #Write into data frame format.
        dt = pd.read_csv(self.out_file_nm)
        df = pd.DataFrame(data=dt)
        df['Date'] = pd.to_datetime(df['Date'], format="mixed")
        df.to_csv('Active_Workfroce.csv')   
        #rows ans columns
        #print(df.columns)
        #print(df.info())
        #df_plt = df[['Date', 'Value']]
        #df_plt.plot()
        #plt.show()
        
        

        
        
    