$(document).ready(function(){
  if(window.location.pathname.indexOf('/login') >= 0){
    var c = $('#content');
    var iframe = '<iframe src="http://www.instructure.com" style="width:647px; height: 400px; margin: 75px auto; display: block;"></iframe>';
    $(iframe).appendTo(c);
  }
});

