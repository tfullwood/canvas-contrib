//////////////////////////////////////////////
/// Hide Conclude Course for certain roles ///
//////////////////////////////////////////////

// Hide the conclude course option.
if  (ENV.current_user_roles.indexOf("teacher") >= 1){
	$("a[href*='confirm_action?event=conclude']").hide();
};