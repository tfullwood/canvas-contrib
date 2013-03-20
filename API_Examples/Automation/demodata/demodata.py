#!/usr/bin/env python

import csv
import sys
import time
from democoursedata import course_data
from random import choice

class DemoMaker(object):
  #user_fieldnames = ('user_id','login_id','password','email','status')
  data = {
      'user':{
        'id_pattern' : "u.%s.%s",
        'fieldnames':('user_id','login_id','password','status'),
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


  def __init__(self,num_users=10):
    self.num_users = num_users
    self.runtime = int(time.mktime(time.localtime())) 

    for k in self.data.keys():
      self.data[k]['headers'] = dict((n,n) for n in self.data[k]['fieldnames']) 
      self.data[k]['create'] = {}
      self.data[k]['delete'] = {}

  def setFile(self,wr_type):
    self.data[wr_type]['create'].setdefault('file',open('./output/create/%s.csv'%wr_type,'wt'))
    self.data[wr_type]['delete'].setdefault('file',open('./output/delete/%s.csv'%wr_type,'wt'))

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
    #writer = csv.DictWriter(user_file,fieldnames=user_fieldnames)
    #writer.writerow(user_headers)
    for x in xrange(int(sys.argv[1])):
      user_id = self.data['user']['id_pattern'] % (self.runtime,x)
      user = dict(
          user_id = user_id,
          login_id = user_id,
          password = self.runtime,
          #email = 'kajigga+%s@gmail.com' % user_id,
          status = 'active')
      self.addData('user',user)

    # Create an account
    acct = {
        'account_id':self.data['account']['id_pattern'] % (self.runtime,'math'),
        'parent_account_id':'',
        'name':'Mathematics %s ' % self.runtime,
        'status':'active'}
    self.addData('account',acct)

    # Create a term
    term = {
        'term_id':self.data['term']['id_pattern'] % (self.runtime,'math'),
        'name':'Math Term %s ' % self.runtime,
        'status':'active'}
    self.addData('term',term)

    # Create a course
    course = dict(
      course_id=self.data['course']['id_pattern'] % (self.runtime, 'math'),
      account_id = acct['account_id'],
      term_id = term['term_id'],
      long_name = 'Math 100',
      short_name = 'math100.%s' % self.runtime,
      status = 'active')
    self.addData('course',course)

    # Create a Section
    section_id = self.data['section']['id_pattern'] % (course['course_id'], '1')
    section = dict(
      section_id=section_id,
      course_id = course['course_id'],
      name = 'Math 100',
      status = 'active')
    self.addData('section',section)

    # Create enrollments for all users, where we have 
    #  - one teacher
    #  - one ta
    #  - one designer
    #  - all the rest as students

    self.addData('enrollment', dict(
      user_id = self.data['user']['create']['data'][0]['user_id'],
      section_id= section_id,
      role = 'teacher',
      status = 'active'))

    self.addData('enrollment', dict(
      user_id = self.data['user']['create']['data'][1]['user_id'],
      section_id= section_id,
      role = 'ta',
      status = 'active'))

    self.addData('enrollment',dict(
      user_id = self.data['user']['create']['data'][2]['user_id'],
      section_id= section_id,
      role = 'designer',
      status = 'active'))  

    for s in self.data['user']['create']['data'][3:]:
      self.addData('enrollment', dict(
        user_id = s['user_id'],
        section_id = section_id,
        role = 'student',
        status = 'active'))
    
    self.writeFiles()
    print "created, password for users is %s" % self.runtime

d = DemoMaker(int(sys.argv[1]))
d.setupDemo()
