Bulk Course Exports
------

This folder contains script samples for bulk exporting content from Canvas in Common
Cartridge format.


python/bulk\_export
------
The first script, python/bulk\_export, simply creates the exports but does not download
them.  It then writes a CSV file out with two columns ```course_id,link_url```.  The
purpose would be to create a file that could be used to do a bulk migration of these
courses into another canvas account.

Ruby
-----
The Ruby bulk export follows the same pattern as the Python script.
