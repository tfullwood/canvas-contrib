Information about the SIS Loader
============================================

This folder contains a script that adds a button to you SIS imports screen. When you click
on this button it will load past SIS import logs on the screen, 10 at a time, and will
continue to load more as you scroll down on the page.

To use this script:

Take all 4 .js files in this folder and host them with your other branding files.
Modify "load_this_file.js", setting the base_url variable to the full URL path of the
folder containing these javascript files.

Add the contents of load_this_file.js to your existing branding javascript file or use it
as the branding javascript file if you don't have another file already.

This script uses dust, a javascript templating library, to generate the HTML on the page.
That is why the dust-core.min.js file is needed.  templates.js contains the compiled
templates themselves.


Support
======

This is an unsupported, community-created project. Keep that in
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.

Good luck!
