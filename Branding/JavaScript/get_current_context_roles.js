/*
 *
 * No Guarantee, No warantee. Use at your own risk
 *
 */
function user_has_role_in_course(role,course_id,callback){
  // Get several pieces of information about the user, course, session, and account
  var user_id = ENV.current_user_id;
  var course_id = $($('li.course_id')[0]).text();
  // Make a call to the api,  This call is authenticated based on the user being logged
  // into Canvas, the cookie/session-based authentication, and the unique page_view_id
  $.ajax({
    url:'https://' + document.location.hostname + '/api/v1/courses/'+course_id+'/enrollments', 
    data: {'type[]':role},
    success: function(d){
      console.log(d);
      for(var x=0; x< d.length; x++){
        if(d[x].user_id == user_id){  // the current user is in the list
          console.log(d);
          callback(true);
          break;
        }
      }
      callback(false);
    },
    dataType: 'json',
  });
}

function do_if_has_role(user,role,course,callback){
  user_has_role_in_course(user,role,course,callback);
}
