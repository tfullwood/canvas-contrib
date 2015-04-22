////////////////////////////////////
//Change the report a problem link//
////////////////////////////////////
$(document).ready(function(){
// set timeout
var tid = setTimeout(mycode, 250);
function mycode() {
  //Change the title of "Ask Your Teacher a Question"
  $("a[href='#create_ticket'] .text").text('Main Text');
  //Change the subtitle of "Questions are submitted to your Teacher"
  $("a[href='#create_ticket'] .subtext").text('SubText');
  tid = setTimeout(mycode, 250); // repeat myself
}
});
