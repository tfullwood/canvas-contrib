/*
 * Hide the "Make this course publicly visible" and
 * "Make the syllabus for this course publicly visible" hidden
 * for non-admins
 */
$(document).ready(function(){
   // Checks that current user role is is a teacher, Admins can see the buttons
  if($.inArray('admin',ENV['current_user_roles']) <= -1) {
    $("input#course_is_public").parent().parent().parent().parent().hide();
  }
});
