$(document).ready(function () {
	$("p:contains(\"Oops, we couldn't find that page.\")").remove();

	$('.submit_error_link.discussion-topic').before('<p>Oops, we couldn\'t find that page. Contact your instructor and let them know that something is missing.</p><p>If you\'re still having a problem email <a href="support@school.edu">support@school.edu</a> for help.</p>');

	$('.submit_error_link.discussion-topic, #submit_error_form').remove();
});