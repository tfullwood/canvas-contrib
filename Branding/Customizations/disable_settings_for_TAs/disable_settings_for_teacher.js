/**
 * JQuery is the javascript library used in many places across canvas.  
 *
 * This script will disable the "Settings" page for TA'a in a course.
 **/
$(document).ready(function(){
  for(x=0;x<ENV.current_user_roles.length;x++){
    if(ENV.current_user_roles[x]=='teacher'){
      $('li.section a.settings').parent().hide();
    }
  }
});
