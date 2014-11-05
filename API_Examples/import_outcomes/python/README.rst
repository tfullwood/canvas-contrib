Import Outcomes
===============

This folder includes a script that reads a CVS file of outcomes into Canvas. 

Requirements
------------

- Python >= 2.4
- requests library http://docs.python-requests.org/en/latest/
- list of outcomes in CSV format

Step 1
------
- create CSV file with the following headers

outcome_id
outcome_group
name
description
mastery_points
<mastery_n>...
<mastery_n>...

The first 5 columns are required and need to be in the order given. There can be any
number of master number columns.  The header are the score to give that ranking, the value
is the text of the outcome rating level.

.. csv-table::
  :file: act_english2.csv

Usage
-------------

[draft]

Create CSV files, run script.  It will prompt for required parameters.
