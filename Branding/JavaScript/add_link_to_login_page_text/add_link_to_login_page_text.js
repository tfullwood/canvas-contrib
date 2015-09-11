///////////////////
//LOGIN PAGE TEXT//
///////////////////

$(document).ready(function(){

  var added_text = '<h5><a href="https://ccsd.instructure.com/profile/observees" target="_blank">Current Parent of user</a>.';
  var added_html_and_text = '<div style="clear:both"><p>' + added_text + '</p></div>';

  $('#login_form').append(added_html_and_text);
});