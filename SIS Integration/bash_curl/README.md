Linux/Unix/Mac OS 10 SIS Integration Example
======

This folder includes examples of code that can be used to integrate
SIS systems with Canvas. These are relatively simple but can serve
as a framework on which you can build.

This script requires the following to be true:

 * *nix system that supports Bash
 * curl with SSL support is installed
 * you know how to connect to said *nix system and can transfer files to it
 * you know how to schedule the task to run regularly with crontab

Setup/Installation
=====

Installation steps:

  * copy the sis_script.sh file to a folder on the *nix system
    * Copy the "csv" folder to the same folder as the sis_script.sh
  * edit sis_script.sh
    * Change the access_token variable
    * change the account_id variable
    * change the domain variables
  * make the script executable
    * chmod +x sis_script.sh


Usage
=====

Create a crontab job to run regularly.  For example, to run this script hourly, you could
create a job like the following:

0 * * * * /path/to/sis_script.sh -e 
  


Support
======

As always, this is provided AS-IS, without warranty, and without any
support beyond this document and anyone kind enough to help from the
community.

This is an unsupported, community-created project. Keep that in 
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.

Good luck!
