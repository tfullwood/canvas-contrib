#!/usr/bin/env python

import json,csv,os
import collections
import time,logging
import requests
import pprint
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
canvas_domain = "yourdomain.test.instructure.com"  # Your Canvas domain.  Use the .test area at first

destination_course_id_column = "destination_id"
num_processes = 4 # Change this to be the number of concurrent course copies to run, with a max of 4
wait_till_done = False # Set this to false if you don't want the script to wait for each
                       # course copy to finish before doing another.

migration_type = "common_cartridge_importer" # Change this to fit your migration type
migration_url_field = 'export_url'
migration_base_url = None # This only needs to be set if linking to files to download from
                          # the web somewhere
process_type = 'upload' # options are 'upload' or 'link'

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

#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.

# I think I should be able to read the field names from the first line
# of the file.  That is assuming the file has headers.  It should always have them.
#

try:
  from clint.textui.progress import Bar
except:
  class Bar(object):
    def __init__(self,*args,**kwargs):
      self.label = kwargs.get('label','')
    def show(self,idx):
      print "{0.label} {1}% done".format(self,idx)

    @property
    def label(self):
      return self._label

    @label.setter
    def label(self, value):
      print value
      self._label = value

# Try loading local config variables from a file called local_config.py.  This file will
# not be in the folder by default.  Rather, it will a file created by the developer.  This
# would really be a special case.
try:
  from local_config import *
except:
  print 'local config file not found'

if "/" in CSVFileName:
   rootLogger.info("The CSVFilename should not contain forwardslashed.  You are warned")

course_copy_queue = []
headers = {"Authorization":"Bearer %s" % token}

def massDoCopies(data):
  # data[1] is the row of data, in the form of a list
  row_data = data[1]

  # data[0] is the progress bar object  
  prog_bar = data[0]
  prog_bar.label = 'doing copy: {}'.format(row_data)

  file_path = os.path.join(workingPath,row_data['source_id'])
  rootLogger.debug(row_data)
  course_search_url = "https://{}/api/v1/courses/{}".format(canvas_domain,row_data['destination_id'])
  rootLogger.info('looking for course: {}'.format(course_search_url))

  done_finding = False
  found_course = {}
  while not done_finding:
    try:
      found_course = requests.get(course_search_url,headers=headers).json()
      done_finding = True
    except:
      pass
  if not found_course.get('id',None):
    rootLogger.error('course {} {}'.format(row_data['destination_id'], 'not found'))
  else:
    rootLogger.info('course found {}'.format(found_course))
    prog_bar.label = 'course found {}'.format(row_data['destination_id'])

    params = {
      'migration_type':migration_type
    }
    if process_type == 'upload':
      params['pre_attachment']={
        'name': row_data['source_id'],
        'name':row_data['source_id'],
        'size':os.path.getsize(file_path), # read the filesize
        'content_type':'application/zip',
       }
      rootLogger.info('='*25+' hello ')
    elif process_type == 'copy':
      # set the source course field
      params['settings'] = {'source_course_id':row_data['source_id']}
    elif process_type == 'link':
      # set the url field
      params['settings'] = {'file_url':row_data['source_id']}

    rootLogger.info(params)

    headers_post = {'Authorization':headers['Authorization'],'Content-type':'application/json'}
    uri = "https://{}/api/v1/courses/{}/content_migrations".format(canvas_domain,row_data['destination_id'])
    rootLogger.info('uri: {}'.format(uri))
    migration = requests.post(uri,headers=headers_post,data=json.dumps(params))
    migration_json = migration.json()
    #result = requests.post(uri,headers=headers,params=params)

    rootLogger.debug(migration.json())
    if process_type=='upload':
      prog_bar.label = 'done triggering course copy, now check status'
      rootLogger.info("Done prepping Canvas for upload, now sending the data...")
      json_res = json.loads(migration.text,object_pairs_hook=collections.OrderedDict)


      # Step 2:  Upload data
      # TODO
      files = {'file':open(file_path,'rb').read()}
      
      _data = json_res['pre_attachment'].items()
      _data[1] = ('upload_params',_data[1][1].items())

      rootLogger.info("Yes! Done sending pre-emptive 'here comes data' data, now uploading the file...")
      upload_file_response = requests.post(json_res['pre_attachment']['upload_url'],data=_data[1][1],files=files,allow_redirects=False)

      # Step 3: Confirm upload

      rootLogger.info("Done uploading the file, now confirming the upload...")
      confirmation = requests.post(upload_file_response.headers['location'],headers=headers)

      if 'id' in confirmation.json():
        file_id = confirmation.json()['id'] 
      else:
        print 'no id here'
        rootLogger.error(confirmation.json())
      rootLogger.info("upload confirmed...nicely done! The Course migration should be starting soon.")

      migration_json = requests.get('https://{}/api/v1/courses/{}/content_migrations/{}'.format(canvas_domain,row_data['destination_id'],migration_json['id']),headers=headers).json()

      
    output = "\r\n" + migration.text
    rootLogger.debug(output)

    pprint.pprint(migration_json)
    prog_url = migration_json['progress_url']
    if wait_till_done:
      status = requests.get(prog_url,headers=headers).json()
      last_progress = status['completion']
      while status['workflow_state'] in ('pre-processing','queued','running'):
        done_statusing = False
        while not done_statusing:
          try:
            status = requests.get(prog_url,headers=headers).json()
            done_statusing = True
          except Exception, err:
            rootLogger.error(err)

        if status['completion']!=last_progress:
          rootLogger.info("{} {}".format(status['workflow_state'],status['completion']))
          last_progress = status['completion']
      rootLogger.info("{} {}".format(status['workflow_state'],status['completion']))
    #copyCache['sources'][source_id].append(csvrow[destination_course_id_column])
    #rootLogger.info('all done')
  return row_data

def runMigrations(copies):
  pool = Pool(processes=num_processes)
  #copies.reverse()

  bar = Bar()
  res = pool.map(massDoCopies,((bar,x) for x in copies))
  #for x in copies:
  #  massDoCopies((bar,x))

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


t = time.strftime("%Y%m%d_%H:%M:%S")

def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

def prep_row(row):

  if process_type == 'link' and migration_base_url:
    source_id = migration_base_url + row.get(source_archive_filename_column,None)
  else:
    source_id = row.get(source_archive_filename_column,"no url given")
  destination_id = row.get(destination_course_id_column,None)
  return source_id,destination_id

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
rootLogger = logging.getLogger('upload_course_migrations')
rootLogger.addHandler(logging.FileHandler(logFilePath))

console = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
rootLogger.addHandler(console)

if __name__ == '__main__':
  rootLogger.info("Log File: {}".format( logFilePath))
  if not os.path.exists(CSVFilePath):
    rootLogger.info('CSVFilePath: {}'.format(CSVFilePath))
    rootLogger.info("`r`n " + t +":: There was no CSV file.  I won't do anything")
  else:
    times = 1
    dr = UnicodeDictReader(open(CSVFilePath,'rU'))
    for csvrow in dr:
      times+=1
      source_id,destination_id = prep_row(csvrow)

      if source_id and destination_id:
        course_copy_queue.append(dict(source_id=source_id,destination_id=destination_id))

    runMigrations(course_copy_queue)

  for h in rootLogger.handlers[:]:
    h.close()
    rootLogger.removeHandler(h)
