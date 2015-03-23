#!/usr/bin/env python

import csv
import os,sys
import time
from democoursedata import course_data
from random import choice
from random_sources import first_names,last_names
import requests
import StringIO

class DemoMaker(object):
  #user_fieldnames = ('user_id','login_id','password','email','status')
  data = {
      'user':{
        'id_pattern' : "u.%s.%s",
        'fieldnames':('user_id','first_name','last_name','login_id','password','status'),
      },
      'course':{
        'id_pattern' : "c.%s.%s",
        'fieldnames' : ('course_id','account_id','term_id','long_name','short_name','status'),
      },
      'section':{
        'id_pattern' : "%s.%s",
        'fieldnames' : ('section_id','course_id','name','status'),
      },
      'account':{
        'id_pattern' : 'a.%s.%s',
        'fieldnames': ('account_id','parent_account_id','name','status'),
      },
      'term':{
        'id_pattern' : "t.%s.%s",
        'fieldnames': ('term_id','name','status'),
      },
      'enrollment':{
        'fieldnames': ('user_id','section_id','role','status')
      }}


  names_list = []
  def __init__(self,num_users=10,num_courses=1,filepath=None):
    self.num_courses = int(num_courses)
    self.num_users = (self.num_courses * 3) + int(num_users)
    self.runtime = int(time.mktime(time.localtime())) 
    if filepath:
        if not os.path.exists(filepath):
            print "filepath {} does not exist".format(filepath)
        if not os.path.exists(os.path.join(filepath,'create')):
            os.mkdir(os.path.join(filepath,'create'))
        if not os.path.exists(os.path.join(filepath,'delete')):
            os.mkdir(os.path.join(filepath,'delete'))

    self.filepath = filepath

    print 'Building %s courses with %s users' % (self.num_courses,self.num_users)

    
    #names_list = requests.get("http://namey.muffinlabs.com/name.json?frequency=rare&count=%d" % self.num_users).json()
    # names_list = requests.get("http://namey.muffinlabs.com/name.json?frequency=rare&count=%d" % 10).json()
    for k in self.data.keys():
      self.data[k]['headers'] = dict((n,n) for n in self.data[k]['fieldnames']) 
      self.data[k]['create'] = {}
      self.data[k]['delete'] = {}

  def getFirstName(self):
    return choice(first_names.FIRST_NAMES)

  def getLastName(self):
    return choice(last_names.LAST_NAMES)

  def getRandomCourse(self):
    random_course = choice(course_data)
    random_course['short_name'].replace(' ','_')
    return random_course

  def setFile(self,wr_type):
    if self.filepath:
        self.data[wr_type]['create'].setdefault('file',open('{}/create/{}.csv'.format(self.filepath,wr_type),'wt'))
        self.data[wr_type]['delete'].setdefault('file',open('{}/delete/{}.csv'.format(self.filepath,wr_type),'wt'))
    else:
        self.data[wr_type]['create'].setdefault('file',StringIO.StringIO(''))
        self.data[wr_type]['delete'].setdefault('file',StringIO.StringIO(''))

  def setWriter(self,wr_type):

    self.setFile(wr_type)
    writer1 = self.data[wr_type]['create'].setdefault('writer',
      csv.DictWriter(self.data[wr_type]['create']['file'],
      fieldnames=self.data[wr_type]['fieldnames']))
    writer1.writerow(self.data[wr_type]['headers'])

    writer2 = self.data[wr_type]['delete'].setdefault('writer',
      csv.DictWriter(self.data[wr_type]['delete']['file'],
      fieldnames=self.data[wr_type]['fieldnames']))
    writer2.writerow(self.data[wr_type]['headers'])

  def addData(self,wr_type,data):
    self.data[wr_type]['create'].setdefault('data',[])
    self.data[wr_type]['delete'].setdefault('data',[])
    self.data[wr_type]['create']['data'].append(data)

    data2 = data.copy()
    data2['status'] = 'deleted'
    self.data[wr_type]['delete']['data'].append(data2)

  def writeFiles(self):
    for k in self.data.keys():
      self.setWriter(k)
      self.data[k]['create']['writer'].writerows(self.data[k]['create']['data'])
      self.data[k]['create']['file'].close()
      self.data[k]['delete']['writer'].writerows(self.data[k]['delete']['data'])
      self.data[k]['delete']['file'].close()

  def setupDemo(self):
    # First create users
    for x in xrange(0,int(self.num_users)):
      user_id = self.data['user']['id_pattern'] % (self.runtime,x)
      user = dict(
          user_id = user_id,
          login_id = user_id,
          password = self.runtime,
          #email = 'kajigga+%s@gmail.com' % user_id,
          first_name = self.getFirstName(),
          last_name = self.getLastName(),
          status = 'active')
      self.addData('user',user)

    # Create an account
    acct = {
        'account_id':self.data['account']['id_pattern'] % (self.runtime,'math'),
        'parent_account_id':'',
        'name':'Online Learning %s ' % self.runtime,
        'status':'active'}
    self.addData('account',acct)
    # Create a sub-account
    sub_acct = {
        'account_id':self.data['account']['id_pattern'] % (self.runtime,'math'),
        'parent_account_id':acct['account_id'],
        'name':'Online Learning Summer 2013%s ' % self.runtime,
        'status':'active'}

    # Create a term
    term = {
        'term_id':self.data['term']['id_pattern'] % (self.runtime,'math'),
        'name':'Math Term %s ' % self.runtime,
        'status':'active'}
    self.addData('term',term)

    current_user = 0
    # Create a course
    courses = []
    sections = []
    for x in range(0,int(self.num_courses)):
      current_user+=1
      random_course = self.getRandomCourse()
      course = dict(
        # TODO Randomly choose a course title
        course_id=self.data['course']['id_pattern'] % (self.runtime, random_course['short_name']),
        account_id = sub_acct['account_id'],
        term_id = term['term_id'],
        long_name = random_course['name'],
        #short_name = 'math100.%s' % self.runtime,
        short_name = '%s: %s' % (random_course['short_name'],self.runtime),
        status = 'active')
      courses.append(course)
      self.addData('course',course)

      # Create a Section
      section_id = self.data['section']['id_pattern'] % (course['course_id'], '1')
      section = dict(
        section_id=section_id,
        course_id = course['course_id'],
        name = "%s [%s]" % (course['long_name'],section_id),
        status = 'active')
      sections.append(section)
      self.addData('section',section)

      teacher =  self.data['user']['create']['data'][current_user]
      # Create enrollments for all users, where we have 
      #  - one teacher
      #  - one ta
      #  - one designer
      #  - all the rest as students

      self.addData('enrollment', dict(
        user_id = teacher['user_id'],
        section_id= section_id,
        role = 'teacher',
        status = 'active'))

      current_user+=1
      ta =  self.data['user']['create']['data'][current_user]
      self.addData('enrollment', dict(
        user_id = ta['user_id'],
        section_id= section_id,
        role = 'ta',
        status = 'active'))

      current_user+=1
      designer =  self.data['user']['create']['data'][current_user]
      self.addData('enrollment',dict(
        user_id = designer['user_id'],
        section_id= section_id,
        role = 'designer',
        status = 'active'))  

    for s in self.data['user']['create']['data'][current_user+1:]:
      self.addData('enrollment', dict(
        user_id = s['user_id'],
        section_id = choice(sections)['section_id'],
        role = 'student',
        status = 'active'))
    
    #self.writeFiles()
    print "created %d courses and %d users. The password for users is %s" % (self.num_courses,self.num_users,self.runtime)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--courses", dest="num_courses",
                      help="number of courses", default=1,metavar="FILE")
    parser.add_option("-u", "--users",
                      dest="num_users", default=10,
                      help="number of users")

    (options, args) = parser.parse_args()
    d = DemoMaker(options.num_users,options.num_courses,filepath='./output/')
    d.setupDemo()
    d.writeFiles()
