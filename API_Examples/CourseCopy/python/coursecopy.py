#!/usr/bin/env python

import json,csv,os
import time
import requests
from multiprocessing import Pool

"""
 You will need to edit several variables here at the top of this script. 
 token = the access token from Canvas
 workingPath = the full working path to where the csv files are created.  
    This is where the logs and archive folders will be created
 CSVFileName = the name of course copy CSV file as it will be created in
    the workingPath.
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

token = "<access_token>" # access_token
workingPath = "/path/to/working/folder/"; # Important! Make sure this ends with a backslash
CSVFileName = "csvfile.csv" # The name of the course copy CSV file.  Not the full path
domain = "<schoolname_test>.instructure.com"
source_course_id_column = "source_id"
destination_course_id_column = "destination_id"
num_processes = 5 # Change this to be the number of concurrent course copies to run at once.  



##############################################################################
##############################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.  

# I think I should be able to read the field names from the first line
# of the file.  That is assuming the file has headers.  It should always have them.
# fieldnames that will exist in the csv file
fieldnames = (source_course_id_column,destination_course_id_column)


debug=False
# Try loading local config variables from a file called local_config.py.  This file will
# not be in the folder by default.  Rather, it will a file created by the developer.  This
# would really be a special case.
try:
  from local_config import *
except:
  print 'local config file not found'
  pass
if "/" in CSVFileName:
    print "The CSVFilename should not contain forwardslashed.  You are warned"

course_copy_queue = []
headers = {"Authorization":"Bearer %s" % token}

def massDoCopies(data):
  print 'doing copies',data[1]

  if not debug:
    params = {'source_course': data[1][0]}
    uri = "https://"+domain+"/api/v1/courses/" + data[1][1] + "/course_copy"
    uri2 = "https://"+domain+"/api/v1/courses/" + data[1][1] 
    #print uri2
    #print uri
    found_course = requests.get(uri2,headers=headers).json()
    if found_course.get('status',None) == 'not_found':
      print 'course ', data[1][1], 'not found'
    else:
      result = requests.post(uri,headers=headers,params=params)

      #print $result
      output = "`r`n" + result.text
      #print output
      #Add-Content -Path $logFilePath -Value $output
      logfile.write(output)
      copyCache['sources'][source_id].append(csvrow[destination_course_id_column])
  else:
    print "would've sent this request",uri,params
    params = {'source_course': data[1][0]}
    uri = "https://"+domain+"/api/v1/courses/" + data[1][1] + "/course_copy"
    print uri
  return data[1]

def runCopies(copies):
  pool = Pool(processes=num_processes)
  res = pool.map(massDoCopies,[(copies,x) for x in copies[1:]])

CSVFilePath = os.path.join(workingPath, CSVFileName)
archivePath = os.path.join(workingPath, "archives")
logPath = os.path.join(workingPath, "logs")

timestamp = time.strftime("%y_%m_%d_%h")
logFilePath = os.path.join(logPath,timestamp + ".log")
cacheFilePath = os.path.join(logPath, "copy_cache.json")
# Create several paths that are needed for the script to run.
# These paths may exist already, but this is a check
if not os.path.exists(archivePath):
    os.mkdir(archivePath)
if not os.path.exists(logPath):
    os.mkdir(logPath)
try:
  os.utime(logFilePath, None)
except:
  open(logFilePath, 'a').close()
 
#if(!(Test-Path -Path $cacheFilePath))
#this sets a default
copyCache = {'sources': {}}
if not os.path.exists(cacheFilePath):

  open(cacheFilePath, 'a').close()
  #json.dump(copyCache,open(cacheFilePath,'wb'))
else:
  print "loading cache from file"
  try:
    copyCache = json.load(open(cacheFilePath,'rb'))
    #print $copyCache.sources
  except ValueError, err:
    #copyCache
    pass

print "Cache File: ", cacheFilePath
print "Log File: ", logFilePath
#$copyCache = ConvertFrom-Json -InputObject $cacheContents

t = time.strftime("%Y%m%d_%H:%M:%S")

def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, fieldnames=('source_id','destination_id'),**kwargs)
  for row in csv_reader:
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

logfile = open(logFilePath,'ab+')
if not os.path.exists(CSVFilePath):
  print CSVFilePath
  print "There was no csv file.  I won't do anything"
  output = "`r`n " + t +":: There was no CSV file.  I won't do anything"
  logfile.write(output)
else:
  times = 1
  for csvrow in UnicodeDictReader(open(CSVFilePath,'rb')):
    print 'times',times
    times+=1
    # TODO: If course::destination is in the cache, don't do it #>
    # Check $obj.sources contains $_.source_id


    source_id = csvrow.get(source_course_id_column,None)
    destination_id = csvrow.get(destination_course_id_column,None)
    copyCache.setdefault('sources',{'%s'%source_id:[]})
    current_source = copyCache['sources'].setdefault(source_id,list())
  
    if source_id and destination_id:

      if destination_id not in copyCache['sources'][source_id]:

        course_copy_queue.append((source_id,destination_id))


  runCopies(course_copy_queue)
	# TODO Write out the json cache again
  print 'writing out the stuff'
  json.dump(copyCache, open(cacheFilePath,'wb'))


  processed_path = os.path.join(archivePath,t+"."+CSVFileName+".processed")
