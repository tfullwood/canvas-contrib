This Python script will programatically do course migrations.  It assumes that you have
saved the files in a folder accessible to the script. Each file will be uploaded to Canvas
then imported into the course.

It requires:

- Python version 2 or above
- Requests Library (http://docs.python-requests.org/en/latest/)

This script also multiprocessing to send multiple course copy API requests at a time. Multiprocessing will be capped to 
4 requests.  This will make it run faster when there are hundred or thousands of copies to do

Setup
======

Step 1: Copy the `upload_course_migrations.py` file to your system.  

Step 2: Edit `upload_course_migrations.py` to change the variables at the top of the file.  
You may also change the source_archive_filename_column and
destination_course_id_column variables.  This will allow you to
customize the script to read the columns you add to the CSV file.

Step 3: Create a CSV file to match the format of the example `csvfile.csv`.  Save this as
whatever you set the `template_filename` to. The format is simple, with only two
columns. *source_filename* is the filename of the course archive.
*destination_id* is the id of the course to receive the content.

	source_filename,destination_id
	some_archive_filename.imscc,somecanvasid


This example uses an SIS id to reference the destination course:

	source_filename,destination_id
	some_archile_filename.imscc,sis_course_id:someothersisid
