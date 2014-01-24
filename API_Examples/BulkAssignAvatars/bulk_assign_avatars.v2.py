#!/usr/bin/python

# For reference, this script can consume a CSV in any format.  It pulls the 
# user ID from the user_id_column column and sets the image as found in user_image_column
# column.

import csv, requests, time

myCsvFile = '<MY_CSV_FILE>' # Example: 'API_Testing/users_provisioning.csv'
myLogFile = '<MY_LOG_FILE>' # Example: '/Users/ianm/Documents/Schools/IMU/log.txt'
domain = '<domain>' # Example: 'coolwebteacher' or 'coolwebteacher.test' for .test
header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}
user_id_column =  'user_id'
user_image_column = 'image_url'

with open(myCsvFile, 'rb') as csvFile:
	csvReader = csv.DictReader(csvFile)
	# Create log object for storing results
	log_time = str(time.asctime(time.localtime(time.time())))
  with open(myLogFile, 'a') as log:
    log.write('\n\n' + log_time + '\n')

    for row in csvReader:
      payload = {'user[avatar][url]' : row[user_image_column]}
      r = requests.put(baseUrl + row[user_id_column], headers = header, params = payload)
      # Output progress to the console
      print str(csvReader.line_num-1) + ". Avatar added for " + row[user_id_column] 
      # Alternatively, write results to a text file
      log.write(str(csvReader.line_num-1) + ". Avatar added for " + row[user_id_column])
