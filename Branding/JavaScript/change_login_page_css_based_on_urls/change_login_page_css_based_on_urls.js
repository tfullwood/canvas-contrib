////////////////////////////////////////////////////////
//Dynamically load login page CSS on different domains//
////////////////////////////////////////////////////////

$(document).ready(function() {
  var head = document.getElementsByTagName('head')[0];
  logo = document.createElement('link');
  logo.type = 'text/css';
  logo.rel = 'stylesheet';

  if (window.location.hostname === "Production URL") {
    logo.href = "URL to different CSS"; //This should be a separate CSS meant for Prod
    head.appendChild(logo);
     }

  if (window.location.hostname === "Test URL") {
    logo.href = "URL to different CSS"; //This should be a separate CSS meant for Test
    head.appendChild(logo);
    }

  if (window.location.hostname === "Beta URL") {
    logo.href = "URL to different CSS"; //This should be a separate CSS meant for Beta
    head.appendChild(logo);
    }
});

/*Change the Forgot Password behavior between different URLs*/

$(document).ready(function() {
  if (window.location.hostname === "Production URL") {
  $("#login_forgot_password").replaceWith("<a href='URL GOES HERE'>Don't know your password?</a>")
  }
  else if (window.location.hostname === "Test URL") {
  $("#login_forgot_password").replaceWith("<a href='URL GOES HERE'>Don't know your password?</a>")
  }
});
