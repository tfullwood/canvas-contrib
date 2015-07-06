$(document).ready(function(){
// set timeout
var tid = setTimeout(mycode, 250);
function mycode() {
  $('.module-sequence-footer-content .pull-left').text("<");
  $('.module-sequence-footer-content .pull-right').text(">");
  tid = setTimeout(mycode, 250); // repeat myself
}
});
