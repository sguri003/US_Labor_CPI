import os            
import json
import requests
import csv
import json
import numpy as np              
import pandas as pd         

FILE_NM = 'states.json'

#states example
#git==>https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-JSON/json_demo.py      
def read_st():
    my_dict = {}
    with open('states.json', 'r')as st:
        my_dict = json.load(st)
        print(my_dict)
        for x in my_dict['states']:
            #print(x['name'], x['abbreviation'], x['area_codes'])
            #del x['area_codes']
            break
    #REMOVING JSON DUMB IF EXISTS. 
    if os.path.exists('new_states.json'):
        os.remove('new_states.json')
        print('File removed')
    else:
        print('Creating File')
    with open('new_states.json', 'w') as f:
        json.dump(my_dict, f, indent=4, sort_keys=True)
    #iterate over all states in JSON sorted
    for k, v in my_dict.items():
        print(k + str(v))
    with open('JSON_CSV.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'area_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in my_dict:
            writer.writerow({'name': key, 'area_code': my_dict[key]})
        
def read_j():
    if os.path.exists('state_format.json'):
        os.remove('state_format.json')
        print('File exists writing JSON dump')
    else:
        print("No file created")
    my_d = {}
    with open('states.json' ,'r') as st_j:
        my_d = json.load(st_j)
        #print(my_d)
    with open('state_format.json' , 'w') as j_df:
        json.dump(my_d,j_df, indent=4, sort_keys=False)
    
    dt = pd.read_json('states.json')
    dt_jFrame = pd.DataFrame(data=dt)
    print(dt_jFrame)
    
read_j()
#read_st()
    

