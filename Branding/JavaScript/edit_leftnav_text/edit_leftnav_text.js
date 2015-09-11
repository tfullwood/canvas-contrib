/*
This snippet allows you to change the text for a link in the left-hand navigation of a course.

<class_name> replace with the class name of the link, which for Canvas links is just the displayed text, but in lowercase.

Links from LTI tools can be updated as well, but their class names will vary, so you'll have to look directly at the HTML. It should look like this though: context_external_tool_<somenumber>
<replacement_text> replace with the new text you want the link to use
*/

$(document).ready(function(){
  $('#section-tabs .<class_name>').text('<replacement_text>');
});
/* Example: $('#section-tabs .quizzes').text('Exams/Quizzes'); */
