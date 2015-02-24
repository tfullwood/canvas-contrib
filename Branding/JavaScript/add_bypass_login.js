
$(document).ready(function(){
  if(window.location.pathname.search('login')){
    //$('#login_forgot_password').text(internal_link_text);
    var new_link = $('<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="/login?canvas_login=1" title="change my password">Internal Canvas Login</a><br/><br/>');
    //$('#login_forgot_password').parent().parent().prepend(new_link);
    //$('label[for=pseudonym_session_remember_me]').after(new_link);
    $('label[for=pseudonym_session_remember_me]').after("<br/><br/>");
    $('#login_forgot_password').after(new_link);
  }
});

