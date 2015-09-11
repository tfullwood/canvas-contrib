//This will hide the right hand side panel when a user is not logged into Canvas

if ($.isEmptyObject(ENV.current_user)) {
  $('#right-side').hide();
};
