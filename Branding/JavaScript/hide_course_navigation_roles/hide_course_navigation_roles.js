//////////////////////////////////////////////
// Hide Course Navigation for certain roles //
//////////////////////////////////////////////

// hide left nav menu options
  if (ENV.current_user_roles.indexOf("admin") == -1 == false){
    $("#section-tabs .outcomes").hide();
    $("#section-tabs .syllabus").hide();
    $("#section-tabs .conferences").hide();
  }
})();