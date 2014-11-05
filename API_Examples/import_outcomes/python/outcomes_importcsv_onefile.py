#!/usr/bin/env python

import requests,json
import argparse
import sys,os
import csv
# Prepare argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--outcomesfile',required=True,help='path to the outcomes.csv file')

domain = "<yourschool>.instructure.com"
token = "<access_token>"
headers = {'Authorization': 'Bearer %s' % token}
#outcomes_fieldnames = ('outcome_id','title','description','mastery_level')
#ratings_fieldnames = ('outcome_id','label','points')

vendor_guid_cache = {'outcome_groups':{},'outcomes':{}}

def checkFileReturnCSVReader(file_name,d=False):
  if not file_name:
    return None
  if os.path.exists(file_name):
    if not d:
      return csv.reader(open(file_name,'rU'))
    else:
      return csv.DictReader(open(file_name,'rU'),fieldnames=('group_id','parent_group_id','title','description'))
  else:
    return None

def getRootOutcomeGroup():
  url = "https://%s/api/v1/accounts/self/root_outcome_group" % domain
  #print 'url',url
  headers2 = {'Authorization': 'Bearer %s' % token}
  return requests.get(url,headers=headers2,verify=False).json()

def paginated_outcomes(outcome_group_id=None):
  # Get outcomes
  all_done = False
  url = 'https://{0}/api/v1/accounts/self/outcome_groups/{1}/outcomes'.format(domain,outcome_group_id)
  while not all_done:
    response = requests.get(url,headers=headers)
    for s in response.json():
      outcome = s['outcome']
      vendor_guid_cache['outcomes'].setdefault(outcome['vendor_guid'],outcome)
      yield outcome 
    if 'next' in response.links:
      url = response.links['next']['href']
    else:
      all_done = True

def paginated_outcome_groups():
  # Get outcome groups 
  all_done = False
  url = 'https://%s/api/v1/accounts/self/outcome_groups' % (domain)
  #params = {}
  while not all_done:
    response = requests.get(url,headers=headers)
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
  url = 'https://%s/api/v1/accounts/self/outcome_groups/%d/subgroups' % (domain,int(parent_group_id))
  #params = {}
  while not all_done:
    response = requests.get(url,headers=headers)
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
      url = response.links['next']['href']
    else:
      all_done = True

do_api_for_find = True
def findOutcomeGroup(outcome_group_id):
  root_group = getRootOutcomeGroup()
  og = vendor_guid_cache['outcome_groups'].get(outcome_group_id,None)
  if do_api_for_find:
    if not og:
      for pog in paginated_outcome_subgroups(root_group['id']):
        if pog['vendor_guid'] == outcome_group_id:
          og = pog
          break
  return og


def getOrCreateOutcomeGroup(outcome_group_id,name,description,parent_group_id=None):
  parent_group = None
  root_group = getRootOutcomeGroup()

  og = vendor_guid_cache['outcome_groups'].get(outcome_group_id,findOutcomeGroup(outcome_group_id))

  if not og:
    if not parent_group_id:
      parent_group = root_group
    else:
      parent_group = vendor_guid_cache['outcome_groups'].get(outcome_group_id,findOutcomeGroup(parent_group_id))

    if not parent_group:
      return None
    else:
      # no outcome group was found, create it now
      og = createOutcomeGroup(outcome_group_id,name,description,parent_group['id'])
  return og

def createOutcomeGroup(vendor_guid,name,description,parent_id):
  url = 'https://%s/api/v1/accounts/self/outcome_groups/%d/subgroups' % (domain,parent_id)
  params = {'title':name,'description':description,'vendor_guid':vendor_guid}
  vendor_guid_cache['outcome_groups'][vendor_guid] = requests.post(url,data=params,headers=headers).json()
  return vendor_guid_cache['outcome_groups'][vendor_guid]

def getOrCreateOutcome(group_id,title,description,vendor_guid,mastery_points,ratings):
    if not vendor_guid_cache['outcomes'].get(vendor_guid,None):
        for outcome in paginated_outcomes(group_id):
            vendor_guid_cache['outcomes'][vendor_guid] = outcome
        if not vendor_guid_cache['outcomes'].get(vendor_guid,None):
            vendor_guid_cache['outcomes'][vendor_guid] = createOutcome(group_id,title,description,vendor_guid,mastery_points,ratings)
    return vendor_guid_cache['outcomes'][vendor_guid]

def createOutcome(group_id,title,description,vendor_guid,mastery_points,ratings):
  path = "/api/v1/accounts/self/outcome_groups/%s/outcomes" % group_id
  params = {
      'title':title,
      'description':description,
      'vendor_guid':vendor_guid,
      'mastery_points':mastery_points,
      'ratings':ratings
      }
  headers = {'Authorization':'Bearer %s'%token,'Content-Type':'application/json'}
  url = 'https://%s%s' % (domain,path)
  res = requests.post(url,headers=headers,data=json.dumps(params))
  return res.json()


if __name__ == '__main__':
    args = parser.parse_args()
    outcomes_file = checkFileReturnCSVReader(args.outcomesfile)
    if outcomes_file :
      outcomes = {}
      outcome_data = {}
      for outcome_row in outcomes_file:

        if outcome_row[0]=="outcome_id":
          # TODO need to make sure this can be a non-canvas id
          outcome_data['rating_levels'] = outcome_row[5:]
          #print 'rating data',outcome_data['rating_levels']
        else:
          # If it's not one of these, assume this is an outcome row
          fields = ['id','outcome_group','name','description','mastery_points']
          outcome = dict(zip(fields,outcome_row[:5]))
          points_description = ['points','description']
          combo = zip(outcome_data.get('rating_levels'),outcome_row[5:])
          outcome['ratings'] = map(lambda x: dict(zip(points_description,x)),combo)
          og = getOrCreateOutcomeGroup(outcome['outcome_group'],outcome['outcome_group'],outcome['outcome_group'])
          if not og:
            print 'OutcomeGroup not found',outcome['outcome_group']
          else:
            outcome['outcome_group_id'] = og['id']
            print "Outcome", getOrCreateOutcome(outcome['outcome_group_id'],
                outcome['name'],
                outcome['description'],
                outcome['id'],
                outcome['mastery_points'],
                outcome['ratings'])['url']
