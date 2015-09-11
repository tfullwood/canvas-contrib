#!/usr/bin/env python
domain = "<domain>.instructure.com"
token = "<token here>"

####################################################################################################
####################################################################################################
############### Don't edit anything after this point unless you know what you
############### are doing. You may know what you are doing, I don't know, but be aware that
############### everything past this point is breakable. You know the "You break it
############### you buy it" kind of thing.
####################################################################################################
####################################################################################################

import requests,json
import argparse
import sys,os
import csv
import pprint

course_id = None # '955508'

def get_headers(with_json=False):
  headers = {'Authorization': 'Bearer %s' % token}
  if with_json:
    headers['Content-Type']='application/json'
  return headers

vendor_guid_cache = {'outcome_groups':{},'outcomes':{}}


def checkFileReturnCSVReader(file_name):
  if file_name and os.path.exists(file_name):
    return csv.reader(open(file_name,'rU'))
  else:
    return None

def getRootOutcomeGroup():
  url = "https://{}/api/v1/courses/{}/root_outcome_group".format(domain,course_id)
  #print 'url',url
  return requests.get(url,headers=get_headers(),verify=True).json()

def paginated_outcomes(outcome_group_vendor_id=None):
  # Get outcomes
  all_done = False
  url = 'https://{0}/api/v1/courses/{2}/outcome_groups/{1}/outcomes'.format(domain,outcome_group_vendor_id,course_id)
  while not all_done:
    response = requests.get(url,headers=get_headers(),verify=True)
    for s in response.json():
      outcome = s['outcome']
      vendor_guid_cache['outcomes'].setdefault(outcome['vendor_guid'],outcome)
      yield outcome 
    if 'next' in response.links:
      url = response.links['next']['url']
    else:
      all_done = True

def paginated_outcome_groups():
  # Get outcome groups 
  all_done = False
  url = 'https://{}/api/v1/courses/{}/outcome_groups'.format(domain,course_id)
  #params = {}
  while not all_done:
    response = requests.get(url,headers=get_headers(),verify=True)
    for s in response.json():
      vendor_guid_cache['outcome_groups'].setdefault(s['vendor_guid'],s)
      yield s
    if 'next' in response.links:
      url = response.links['next']['href']
    else:
      all_done = True

def paginated_outcome_subgroups(parent_group_id):
  # Get outcome subgroups (this needs to walk)

  all_done = False
  url = 'https://%s/api/v1/courses/%s/outcome_groups/%d/subgroups' % (domain,course_id,int(parent_group_id))
  #params = {}
  while not all_done:
    response = requests.get(url,headers=get_headers(),verify=True)
    if not response.json():
      #yield []
      return
    else:
      for s in response.json():
        yield s
        vendor_guid_cache['outcome_groups'].setdefault(s['vendor_guid'],s)
        for sg in paginated_outcome_subgroups(s['id']):
          vendor_guid_cache['outcome_groups'].setdefault(s['vendor_guid'],s)
          yield s
    if 'next' in response.links:
      url = response.links['next']['url']
    else:
      all_done = True

do_api_for_find = True
def findOutcomeGroup(outcome_group_vendor_id):
  root_group = getRootOutcomeGroup()
  og = vendor_guid_cache['outcome_groups'].get(outcome_group_vendor_id,None)
  if do_api_for_find:
    if not og:
      for pog in paginated_outcome_subgroups(root_group['id']):
        if pog['vendor_guid'] == outcome_group_vendor_id:
          og = pog
          break
  return og

def deleteOutcomeGroup(outcome_group_id):
  url = 'https://%s/api/v1/courses/%s/outcome_groups/%d' % (domain,course_id,outcome_group_id)
  return requests.delete(url,headers=get_headers(),verify=True)

def getOrCreateOutcomeGroup(outcome): #outcome_group_vendor_id,name,description,parent_group_id=None):
  parent_group = None
  root_group = getRootOutcomeGroup()

  # print 'root_group',root_group # This is good

  outcome_group_vendor_id = outcome['outcome_group_vendor_guid']
  name = outcome['outcome_group_vendor_guid']
  description = outcome['outcome_group_vendor_guid']
  parent_group_id = outcome['parent_outcome_group_vendor_guid']
  print 'requested parent_group_id',parent_group_id

  og = vendor_guid_cache['outcome_groups'].get(outcome_group_vendor_id,findOutcomeGroup(outcome_group_vendor_id))

  if not og:
    if not parent_group_id:
      parent_group = root_group
    else:
      parent_group = vendor_guid_cache['outcome_groups'].get(outcome_group_vendor_id,findOutcomeGroup(parent_group_id))

    print '======= parent_group',parent_group
    if not parent_group:
      return None
    else:
      # no outcome group was found, create it now
      og = createOutcomeGroup(outcome,parent_group['id'])
  return og

def createOutcomeGroup(outcome,parent_id):
  vendor_guid = name = outcome['outcome_group_vendor_guid']
  description = outcome['description']
  url = 'https://%s/api/v1/courses/%s/outcome_groups/%d/subgroups' % (domain,course_id,parent_id)
  params = {'title':name,'description':description,'vendor_guid':vendor_guid}
  vendor_guid_cache['outcome_groups'][vendor_guid] = requests.post(url,data=params,headers=get_headers(),verify=True).json()
  return vendor_guid_cache['outcome_groups'][vendor_guid]

def getOrCreateOutcome(outcome_to_create):
  if not vendor_guid_cache['outcomes'].get(outcome_to_create['vendor_guid'],None):
    for outcome in paginated_outcomes(outcome_to_create['group_id']):
      vendor_guid_cache['outcomes'][outcome['vendor_guid']] = outcome
    if not vendor_guid_cache['outcomes'].get(outcome_to_create['vendor_guid'],None):
      vendor_guid_cache['outcomes'][outcome_to_create['vendor_guid']] = createOutcome(outcome_to_create)#group_id,title,description,vendor_guid,mastery_points,ratings)
  return vendor_guid_cache['outcomes'][outcome_to_create['vendor_guid']]

#def createOutcome(group_id,title,description,vendor_guid,mastery_points,ratings):
def createOutcome(outcome_to_create):
  path = "/api/v1/courses/%s/outcome_groups/%s/outcomes" % (course_id,outcome_to_create['group_id'])

  post_headers = {'Content-Type':'application/json'}
  url = 'https://%s%s' % (domain,path)
  
  #data = json.dumps(outcome_to_create)
  res = requests.post(url,headers=get_headers(with_json=True),data=json.dumps(outcome_to_create),verify=True)
  return res.json()

def updateOutcome(outcome_to_update):
  path = "/api/v1/courses/%s/outcome_groups/%s/outcomes/%s" % (course_id,outcome_to_update['outcome_group']['id'],outcome_to_update['outcome']['id'])
  headers = {'Authorization':'Bearer %s'%token,'Content-Type':'application/json'}
  url = 'https://%s%s' % (domain,path)
  res = requests.put(url,headers=get_headers(),data=outcome_to_update,verify=True)
  del(vendor_guid_cache['outcomes'][outcome_to_update['outcome']['vendor_guid']])
  return res.json()



def isValidRow(row):
  return len(row) >=9


# Prepare argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--outcomesfile',required=True,help='path to the outcomes.csv file')
parser.add_argument('--course',required=True,help='course id where the outcomes should go')
ratings_column = 8
if __name__ == '__main__':
    args = parser.parse_args()
    outcomes_file = checkFileReturnCSVReader(args.outcomesfile)
    course_id = args.course
    if outcomes_file :
      outcomes = {}
      outcome_data = {}
      for outcome_row in outcomes_file:
        
        if outcome_row[0]=="vendor_guid":
          # TODO need to make sure this can be a non-canvas id
          outcome_data['rating_levels'] = outcome_row[ratings_column:]
          #print 'rating data',outcome_data['rating_levels']
        else:
          # If it's not one of these, assume this is an outcome row
          fields = ['vendor_guid','outcome_group_vendor_guid','parent_outcome_group_vendor_guid','title','description','calculation_method','calculation_int','mastery_points']
          outcome = dict(zip(fields,outcome_row[:ratings_column]))
          points_description = ['points','description']

          combo = zip(outcome_data.get('rating_levels'),outcome_row[ratings_column:])
          outcome['ratings'] = map(lambda x: dict(zip(points_description,x)),combo)
          if outcome_row[0] == '':
            getOrCreateOutcomeGroup(outcome)
          else:
            og = getOrCreateOutcomeGroup(outcome)#['outcome_group'],outcome['outcome_group'],outcome['outcome_group'])
            outcome['group_id'] = og['id']
            if not og:
              print 'OutcomeGroup not found',outcome['outcome_group']
            else:
              outcome['outcome_group_vendor_id'] = og['id']
              print 'outcome_to_create',outcome['vendor_guid']
              print "Outcome", getOrCreateOutcome(outcome)
