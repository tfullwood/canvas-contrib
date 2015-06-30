from unittest import TestCase
import os
import uuid

from outcomes_importer import checkFileReturnCSVReader
from outcomes_importer import isValidRow
from outcomes_importer import createOutcome
from outcomes_importer import getOrCreateOutcomeGroup
from outcomes_importer import deleteOutcomeGroup
#from outcomes_importer.outcomes_importercsv_onefile import checkFileReturnCSVReader

class OutcomeImporterTests(TestCase):
  def setUp(self):
    self.path_to_valid_file = "./tests/act_english_calculatio_method.csv"
    self.outcome_group = None
    self.outcome_vendor_guid = uuid.uuid4().hex
    self.outcome_group_vendor_guid = uuid.uuid4().hex

  def tearDown(self):
    print 'hello from tearDown'
    # TODO Delete outcome and outcome groups if they are created
    if self.outcome_group:
      # TODO delete it
      print deleteOutcomeGroup(self.outcome_group['id'])

  def test_check_file_exists(self):
    '''
    vendor_guid	outcome_group_vendor_guid	parent_outcome_group_vendor_guid	title	description	calculation_method	calculation_int	mastery_points	1	2	3	4
    '''
    self.assertTrue(os.path.exists(self.path_to_valid_file))
    outcomes_file = checkFileReturnCSVReader(self.path_to_valid_file)
    self.assertTrue(outcomes_file)
    
  def test_check_validates_first_row(self):
    outcomes_file = checkFileReturnCSVReader(self.path_to_valid_file)
    first_row = outcomes_file.next()
    fields = ('vendor_guid','outcome_group_vendor_guid','parent_outcome_group_vendor_guid','title','description','calculation_method','calculation_int','mastery_points','1','2','3','4')
    for idx,f in enumerate(fields):
      self.assertEqual(first_row[idx],f)

    second_row = outcomes_file.next()
    self.assertTrue(isValidRow(second_row))

  def test_create_outcome(self):
    outcome = {
      'title':'test outcome',
      'description':'test description',
      'vendor_guid':'test_guid_{}'.format(self.outcome_vendor_guid),
      'outcome_group_vendor_guid':'test_group_guid_{}'.format(self.outcome_group_vendor_guid),
      'mastery_points':5,
      #'ratings':
      'calculation_method':'decaying_average',
      'calculation_int':'75'
      }

    self.outcome_group = getOrCreateOutcomeGroup(outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'])
    self.assertTrue(self.outcome_group.has_key('id'))

    outcome['group_id'] = self.outcome_group['id']
    o = createOutcome(outcome)
    self.assertTrue(o.has_key('outcome'),msg=o)
    self.assertTrue(o['outcome'].has_key('id'),msg=o)

