/*
 * Use this to remove the Delete Course, Conclude Course, and Reset Course Content 
 * Buttons from Canvas if you are a teacher
 */

//This hides the buttons
$(document).ready(function(){
   // Checks that current user role is is a teacher, Admins can see the buttons
  if($.inArray('teacher',ENV['current_user_roles']) === 1) {
    $('a.btn.button-sidebar-wide.delete_course_link').hide();
    $('a.btn.button-sidebar-wide.reset_course_content_button').hide();
    $("a:contains('Conclude this Course')").hide();
  }
});
