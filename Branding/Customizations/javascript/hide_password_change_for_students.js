/*
 * This script will hide the password change option that appears in settings for students.  Teachers, admins, and observers will still have the ability to change the password.
 *
 * It appears to work well but use at your own risk.
 */

$(document).ready(function(){
  // If the user is a student in the course, but is not a teacher or admin elsewhere hide the change password field


  if($.inArray('student',ENV['current_user_roles']) == 1 && $.inArray('teacher',ENV['current_user_roles']) == -1 && $.inArray('admin',ENV['current_user_roles']) == -1) {
    $('.select_change_password_row').remove();
  }
});
