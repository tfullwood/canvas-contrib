Prevent Students Printing Quizzes
==================================

This set of files will allow you to prevent (note: not block) students from printing
quizzes.  What it does is load a CSS file in the browser when a student takes a quiz.
This CSS file does just one thing, make the body of the page invisible when printed.

In order to get this to work, you will need to follow the following steps:

#.  Download the noprint.css file.  Upload it to the same location as your other branding
    files.  Make a note of the full URL of this CSS file.

#.  Download the prevent_printing_quizes.js.  If you already have a javascript
    branding file in use with your Canvas account then add this content to that file.  
#.  Edit the javascript. Modify the line that starts with *var base_url_for_links =*  
    to contain the URL to where the noprint.css file is located at.  Include everything up
    to but not including the *noprint.css* part.

    e.g. "https://s3.amazonaws.com/SSL_Assets/kevin/css/"

#.  Upload the file to your branding location, make a note of the URL of the javascript
    file and enter this URL into your Canvas branding field.  

NOTE: **You should not put the link to the noprint.css file in your Canvas CSS branding field.**



