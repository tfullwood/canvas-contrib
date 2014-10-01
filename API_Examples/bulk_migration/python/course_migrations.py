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

source_archive_filename_column = "source_filename"
migration_base_url = "https://dl.dropboxusercontent.com/u/1647772/migration_files/" # The base URL for finding course archives.  This should end with a forward slash "/"
canvas_domain = "yourdomain.test.instructure.com"  # Your Canvas domain.  Use the .test area at first

destination_course_id_column = "destination_id"
num_processes = 4 # Change this to be the number of concurrent course copies to run at once.  
wait_till_done = False # Set this to false if you don't want the script to wait for each
                       # course copy to finish before doing another.

migration_type = "common_cartridge_importer" # Change this to fit your migration type

""" Recent options for migration_type include:
"type": "angel_exporter",
"name": "Angel export .zip format",

"type": "blackboard_exporter",
"name": "Blackboard 6/7/8/9 export .zip file",

"type": "webct_scraper",
"name": "Blackboard Vista/CE, WebCT 6+ Course",

"type": "canvas_cartridge_importer",
"name": "Canvas Course Export Package",

"type": "common_cartridge_importer",
"name": "Common Cartridge 1.0/1.1/1.2 Package",

"type": "d2l_exporter",
"name": "D2L export .zip format",

"type": "moodle_converter",
"name": "Moodle 1.9 .zip file",
]
"""

##############################################################################
##############################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.  

# I think I should be able to read the field names from the first line
# of the file.  That is assuming the file has headers.  It should always have them.
# fieldnames that will exist in the csv file


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

def _o(_str):
  if _str and debug:
    logfile.write(str)
  print _str
  


course_copy_queue = []
headers = {"Authorization":"Bearer %s" % token}

def massDoCopies(data):
  print 'doing copies',data[1]

  if not debug:
    params = {
      'settings[file_url]': data[1][0],
      'migration_type':migration_type
      }
    uri = "https://"+canvas_domain+"/api/v1/courses/" + data[1][1] + "/content_migrations/"
    uri2 = "https://"+canvas_domain+"/api/v1/courses/" + data[1][1] 
    output = 'looking for course'

    print output
    logfile.write(output)
    logfile.write(str(params))
    done_finding = False
    while not done_finding:
      try:
        found_course = requests.get(uri2,headers=headers).json()
        done_finding = True
      except:
        pass
    if not found_course.get('id',None):
      print 'course ', data[1][1], 'not found'
      logfile.write('course '+ data[1][1]+ ' not found')
    else:
      print 'course found',found_course
      done_posting = False
      while not done_posting:
        try:
          result = requests.post(uri,headers=headers,params=params)
          done_posting = True
        except:
          pass
      print 'done triggering course copy, now check status'


      #print $result
      output = "\r\n" + result.text
      logfile.write(output)

      ## TODO update this to content_migration statusing
      uri3 =  result.json()['progress_url']
      done_statusing = False
      while not done_statusing:
        try:
          status = requests.get(uri3,headers=headers).json()
          done_statusing = True
        except:
          pass
      if wait_till_done:
        last_progress = status.get('progress',None)
        while status['workflow_state'] in ('queued','running'):
          done_statusing = False
          while not done_statusing:
            try:
              status = requests.get(uri3,headers=headers).json()
              done_statusing = True
            except:
              pass
          
          if status['completion']!=last_progress:
            #print ''
            print status['workflow_state'],status['completion']
            last_progress = status['completion']
          else:
            pass
            #print status['workflow_state'],status['completion']
            #print '.',
        print status['workflow_state'],status['completion']
      #copyCache['sources'][source_id].append(csvrow[destination_course_id_column])
  else:
    params = {'source_course': data[1][0]}
    uri = "https://"+canvas_domain+"/api/v1/courses/" + data[1][1] + "/content_migrations"
    print "would've sent this request",uri,params
    print uri
  return data[1]

def runMigrations(copies):
  pool = Pool(processes=num_processes)
  copies.reverse()
  #print 'hh'
  res = pool.map(massDoCopies,[(copies,x) for x in copies])

CSVFilePath = os.path.join(workingPath, CSVFileName)
archivePath = os.path.join(workingPath, "archives")
logPath = os.path.join(workingPath, "logs")

timestamp = time.strftime("%y_%m_%d_%h")
logFilePath = os.path.join(logPath,timestamp + ".log")
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
 
print "Log File: ", logFilePath

t = time.strftime("%Y%m%d_%H:%M:%S")

def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    print row
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

logfile = open(logFilePath,'ab+')
if __name__ == '__main__':
  if not os.path.exists(CSVFilePath):
    print CSVFilePath
    print "There was no csv file.  I won't do anything"
    output = "`r`n " + t +":: There was no CSV file.  I won't do anything"
    logfile.write(output)
  else:
    times = 1
    dr = UnicodeDictReader(open(CSVFilePath,'rb'))
    #dr.next()
    for csvrow in dr:
      times+=1
      # Check $obj.sources contains $_.source_id


      source_id = migration_base_url + csvrow.get(source_archive_filename_column,None)
      destination_id = csvrow.get(destination_course_id_column,None)
    
      if source_id and destination_id:

        course_copy_queue.append((source_id,destination_id))


    #print course_copy_queue
    runMigrations(course_copy_queue)

