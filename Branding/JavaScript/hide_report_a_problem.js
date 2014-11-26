$(document).ready(function(){

  // Only hide "Report a Problem" for student users
  if(ENV.current_user_roles.indexOf("student") > -1) {
  
    $('.help_dialog_trigger').click(function(){
      // Create a timer to check for the report a problem link, as soon as it exists, remove
      // it and stop the timer. The script shouldn't run forever looking for the link.

      var timeoutSeconds=5; // script timeout, 5 seconds is good
      var date = new Date(); // Create the date object, used for measuring the timeout
      var startTime = date.getTime(); // capture the startTime, used for measuring the timeout
      var link_to_hide,timerid;  // create a few variables, setting them to null

      var checkForLink = function(){
        var diff = date.getTime()-startTime; // How many milliseconds have passed...
        // Search for the link and pick the parent object
        link_to_hide = $('#help-dialog-options a[href=#create_ticket]').parent();  
        /* If more than timeoutSeconds*1000 (milliseconds) has passed or if
         * link_to_hide.length is found, hide the link and stop looking for it */
        if(diff >= timeoutSeconds*1000 || (link_to_hide && link_to_hide.length!==0)){
          link_to_hide.hide();
          clearInterval(timerid);
        }
      }
      /* Start an interval (timer) to look for the link every 100 milliseconds. We can't just search for the link immediately
       * because it is loaded dynamically when the "Help" button is clicked. */
      timerid = setInterval(checkForLink,100);
    });
  
  }

});