$(document).ready(function() {
	//console.log("ADDING STUDENT SUPPORT LINK!");
	$("#menu").append("<li id='support_menu_item' class='menu-item'><a class='menu-item-no-drop'>Student Support</a></li>");

	var div = function(body) { return "<div id='support-dialog' title='Support'>"+body+"</div>" }
	var content = "<div><p><h4>Can we help you? Student Support is only a phone call or email away! From navigating your course, submitting lessons, to requesting an exam, we are here to help.</h4></p><br/>";
	content += "<p>E-mail: <a href='mailto:MizzouK12Online@missouri.edu'>test</a></p>";
	content += "<p>Phone: 1-855-256-4975 (toll-free)</p><br/>";
	content += "<h4>Office Hours (August 9th - May 17th)</h4>";
	content += "<p>Monday-Friday 8AM-5PM Central Time</p>";
	content += "<h4>Summer Office Hours (May 18th to August 10th)</h4>";
	content += "<p>Monday-Friday 7:30AM-4PM Central Time</p>";
	content += "</div>";

	console.log("ADDING CLICK HANDLER!");
	$("#support_menu_item").children(".menu-item-no-drop").click(function(){
		//console.log("CLICKED!");
		//$("#content").empty();
		$("#content").append(div(content));


		$("#support-dialog").dialog({
			maxWidth: 600,
			maxHeight: 500,
			width: 600,
			height: 500,
			modal: true,
			buttons: {
				OK: function() {
					$(this).dialog("close");
				}
			}
		});
	});
});
