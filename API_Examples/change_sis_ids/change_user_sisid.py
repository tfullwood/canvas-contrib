#!/usr/bin/env python

import requests, json
import csv

""" Example change_users.csv file

old_user_id,new_user_id
201.bobby,2013.bobby

"""

filename = 'change_users.csv' # Change this to the file with the two columns
domain = '<some_domain>.instructure.com' # Change this
token = '<your_token_here>' # Change this


 
# Read CSV file

headers = {'Authorization':'Bearer %s' % token}
user_list = csv.DictReader(open(filename,'rb'))
for user in user_list:
  # Get the logins for the user, find the one with the old SIS id, and change it
  url = 'https://%s/api/v1/users/sis_user_id:%s/logins' % (domain,user['old_user_id'])

  login_response = requests.get(url,headers=headers)
  logins = login_response.json()
  if type(logins) != list:
    print "the user probably wasn't found, keep going"

  else:
    for l in logins:
      try:
        if l['sis_user_id'] == user['old_user_id']:
          params = {'login[sis_user_id]':user['new_user_id']}
          url = 'https://%s/api/v1/accounts/self/logins/%s' % (domain,l['id'])
          updated_login_response = requests.put(url,headers=headers,params=params)
          print updated_login_response.json()
      except Exception, exc:
        print logins
        print "The user probably wasn't found.  Keep going..."


