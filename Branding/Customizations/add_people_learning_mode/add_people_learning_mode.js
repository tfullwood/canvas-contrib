$(document).ready(function () {

	/***********************************************
	 ** People: Add Face Book and Learning Mode
	 ***********************************************/
	// Url must match this pattern
	if (window.location.href.match(/\/courses\/\d+\/users/ig)) {
		// Listen for completion of all AJAX calls, then insert the Learning Mode button
		$(document).ajaxComplete(function () {
			if ($("#wms_roster_btn_learning").length == 0) {

				// Insert the Learning Mode button
				$("DIV#content.container-fluid DIV DIV.v-gutter TABLE.roster").before('<div id="wms_roster_controls"><button id="wms_roster_btn_learning" class="btn btn-small" title="(Photos viewable on-campus or via VPN)"><i class="icon-user"></i> Show Face Book</button>&nbsp;&nbsp;<a href="#" id="wms_roster_toggle_names" title=""></a><br /><br /></div>');

				// Provide custom instructions for the "Add People" modal dialog (careful: modal is not initially in DOM; it is created on the fly by Canvas)
				$("#addUsers").click(function(evt){
					$("#create-users-step-1 p").text("Enter Unix names or Williams long-style email addresses. (Avoid short email format: ob1@williams.edu)");
					$("#user_list_textarea").prop("placeholder", "ob1, pleia, Anakin.Skywalker@williams.edu, Jabba.T.Hutt@williams.edu");
				});
			}
			else {
				// Avoid creating duplicate buttons
				return false;
			}

			// Toggle: Learning Mode button
			$("#wms_roster_btn_learning").toggle(function (event) {

				// Turn learning mode: ON
				$("#wms_roster_btn_learning").html("<i class=\"icon-user\"></i> Return to List");

				// Initial state of hyperlink
				$("#wms_roster_toggle_names").text("Turn Learning Mode On").prop("title", "Hide names");

				// Toggle: Names hyperlink
				$("#wms_roster_toggle_names").toggle(function (event) {
					// Hide the name/role
					$("#wms_roster_toggle_names").text("Turn Learning Mode Off").prop("title", "Show names");
					$(".wms_roster_user small").addClass("hide");
					// Display name/role upon image hover
					$("#wms_roster_grid .wms_roster_user").hover(function () {
						$(this).find("small").removeClass("hide");
					}, function () {
						$(this).find("small").addClass("hide");
					});
				}, function () {
					// Show the name/role
					$("#wms_roster_toggle_names").text("Turn Learning Mode On").prop("title", "Hide names");
					$(".wms_roster_user small").removeClass("hide");
					// Display name/role upon image hover
					$("#wms_roster_grid .wms_roster_user").hover(function () {
						$(this).find("small").removeClass("hide");
					}, function () {
						$(this).find("small").removeClass("hide");
					});
				});

				// Create array to copy desired contents
				var createGrid = "";
				var extractHTMLObjects = $("TABLE.roster TBODY TR.rosterUser");
				$.each(extractHTMLObjects, function (index, value) {
					// console.log(index + "/" + $(value).html()); // produces: 5/[object HTMLTableCellElement]
					var img = $(this).find('td:nth-child(1)').html();
					var name = $(this).find('td:nth-child(2)').html();
					var role = $(this).find('td:nth-child(5)').text();

					var user_info = img + "<small class=\"\">" + name + "</small><br /><small class=\"\">" + role + "</small>";
					createGrid += "<div class=\"wms_roster_user\">" + user_info + "</div>";
				});
				createGrid = "<div id=\"wms_roster_grid\">" + createGrid + "</div>";

				// Display grid (add it to DOM)
				$("TABLE.roster.table.table-hover.table-striped.table-condensed.table-vertically-center").before(createGrid);
				// Hide Canvas default student table
				$("TABLE.roster.table.table-hover.table-striped.table-condensed.table-vertically-center").addClass("hide");
			}, function () {
				// Turn learning mode: OFF
				$("#wms_roster_btn_learning").html("<i class=\"icon-user\"></i> Show Face Book").prop("title", "(Photos viewable on-campus or via VPN)");
				// Remove Link: Hide Names
				$("#wms_roster_toggle_names").text("").prop("title", "");
				// Remove grid from DOM
				$("#wms_roster_grid").remove();
				// Restore Canvas default student table
				$("TABLE.roster.table.table-hover.table-striped.table-condensed.table-vertically-center").removeClass("hide");
			});

		}); // END OF: (document).ajaxComplete
	}


}); // END OF: (document).ready
