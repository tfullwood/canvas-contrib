//This is an unsupported community script
//Functional on new Canvas UI as of 12/29/15

$(document).ready(function () {
	var forgot_password = getQueryVariable("forgot_password");

	function getQueryVariable(variable) {
	  var query = window.location.search.substring(1);
	  var vars = query.split("&");
	  for (var i=0;i<vars.length;i++) {
	    var pair = vars[i].split("=");
	    if (pair[0] == variable) {
	      return pair[1];
	    }
	  } 
	}

	if (forgot_password == "1") {
	    $('#login_form').hide();
	    $('#forgot_password_form').show();
	}
});