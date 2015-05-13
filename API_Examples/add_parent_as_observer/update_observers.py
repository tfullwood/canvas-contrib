#!/usr/bin/python

'''
For reference column headers must be
parent_id,student_id
'''

myCsvFile = '/Users/kevin/Desktop/observer.csv' # Example: 'API_Testing/users_provisioning.csv'
domain = 'kevin.instructure.com'
token = '1~p4FW4DfznOqpftUVxoC5KFYRxi4ck0RMhriFmO1CydoIJwsjkp463EH73lq0XeCP' 


#### Don't edit past this unless you know what you're doing
import csv, requests
header = {'Authorization' : 'Bearer {}'.format(token)}

with open(myCsvFile, 'rb') as csvFile:
  csvReader = csv.DictReader(csvFile)
  
  for row in csvReader:
    baseUrl = 'https://{0}/api/v1/users/{1[parent_id]}/observees/{1[student_id]}'.format(domain,row) 
    r = requests.put(baseUrl, headers = header)
    # Output progress to the console
    print r.json()
