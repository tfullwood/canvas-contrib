/*
  This snippet allows you to change the color of a course/courses listed in the Courses dropdown, 
  based off a keyword in the course name
	
  Originally used because an institution wanted their template/master courses (with "Template" in the name) 
  to stick out separately from their other courses

  <KEYWORD> replace with the text string the course(s) in question contain(s)
  <COLOR> replace with the color you'd like to change the course name to. Can be color name ("green"), hex value ("#2E9524"), etc.
*/

$(document).ready(function(){
  $("ul.menu-item-drop-column-list li.customListItem span.ellipsis:contains('<KEYWORD>')").css("color", "<COLOR>");
});



