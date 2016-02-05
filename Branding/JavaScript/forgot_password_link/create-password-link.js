//This is an unsupported community script
//Functional on new Canvas UI as of 12/29/15

$(document).ready(function () {
	var create_password = getQueryVariable("create_password");

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

	if (create_password == "1") {
	    $('#login_form').hide();
	    $('#forgot_password_form').show();
	    $('#forgot_password_instructions').html('Enter your institution provided email address to create your password. After submitting the form check your inbox and follow the instructions provided in the email.');
	}
});