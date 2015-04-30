//This script changes the word Quizzes to Assessments

$(document).ready(function(){
  $("a.quizzes").text('Assessments');
});

$(document).ready(function(){
  $("li.navitem.enabled.quizzes").text('Assessments');
});


$(document).ready(function() {
	$("title:contains('Quizzes')").text("Assessments");
    $("span:contains('Quizzes')").text("Assessments");
    $("h2:contains('Quizzes')").text("Course Assessments");
    //$("#content:contains('quizzes')").text("assessments");
});
