/*
 *
 * No Guarantee, No warantee. Use at your own risk
 *
 */
$(document).ready(function(){
  // Only run this if we are looking at a course
  if(ENV.context_asset_string.search('course')>=0){
    // Get several pieces of information about the user, course, session, and account
    var pvid = $(page_view_id).text(); // 
    var act_id = $(domain_root_account_id).text();
    var user_id = ENV.current_user_id;
    var course_id = $($('li.course_id')[0]).text();
    // Find the settings tab
    var settings_tab = $('li.section').has('a.settings');
    // and hide it
    settings_tab.hide();
    // Make a call to the api,  This call is authenticated based on the user being logged
    // into Canvas, the cookie/session-based authentication, and the unique page_view_id
    $.ajax({
      url:'https://' + document.location.hostname + '/api/v1/courses/'+course_id+'/enrollments', 
      data: { page_view_id:pvid,"type[]":'TaEnrollment'},// Get just TA Enrollments for this course
      success: function(d){
        var in_list = false;
        for(var x=0; x< d.length; x++){
          if(d[x].user_id == user_id){  // the current user is in the list
            console.log(d);
            in_list = true;  // set this to true
            break;
          }
        }
        if(in_list===false){  // if the current user wasn't found in the list, show the settings tab again
          // Show the settings tab, I'm not a TA
          settings_tab.show();
        }
      },
      dataType: 'json',
      error: function(){  // Just show the settings tab when an error occurs
        settings_tab.show();
      }
    });
  }
});
