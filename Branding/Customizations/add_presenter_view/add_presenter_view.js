$(document).ready(function () {

	/***********************************************
	 ** Add Presenter View (zoom content area; hide all other columns)
	 ***********************************************/
	$("NAV#breadcrumbs UL LI").last().after('<li style="float:right; background-image:none;"><div id="wms_presenter_exit_btn"><div id="wms_presenter_exit_text" class="wmsPresenterRotate wmsDisplayNone">Exit&nbsp;Presenter&nbsp;View</div><a id="wms_presenter_breadcrumb" class="btn-mini" href="#" title="Enable Presenter View"><i class="icon-off"></i> Presenter View</a>&nbsp;&nbsp;</div></li>');

	// Presenter View: Create custom toggle click state
	(function ($) {
		$.fn.togglePresenterView = function () {
			var ele = this;
			ele.data('clickState', 0);
			ele.click(function () {
				//This will only set this._originalHeight once (value is stored in the DOM node itself)
				this._originalHeight = this._originalHeight || $("DIV#main").height();
				if (ele.data('clickState')) {
					// show breadcrumb link and page elements
					$("#wms_presenter_breadcrumb").removeClass("wmsDisplayNone");
					$("DIV#header").removeClass("wmsDisplayNone");
					$("DIV#left-side").removeClass("wmsDisplayNone");
					$("DIV#right-side-wrapper").removeClass("wmsDisplayNone");
					$("FOOTER").removeClass("wmsDisplayNone");
					// hide zoom
					$("DIV#main").removeClass("wmsMarginZero").removeClass("wmsPresenterZoom");
					// reset height to original value (temporary height * 0.5 modifier to undo the previous zoom)
					$("DIV#main").css('cssText', 'min-height: ' + this._originalHeight + 'px !important;');
					// hide exit button
					$("#wms_presenter_exit_btn").removeClass("wmsPresenterExit").prop("title","Enable Presenter View");
					$("#wms_presenter_exit_text").addClass("wmsDisplayNone");
					// scroll to top of page
					$("HTML,BODY").scrollTop(0);
				} else {
					// hide breadcrumb link and page elements
					$("#wms_presenter_breadcrumb").addClass("wmsDisplayNone");
					$("DIV#header").addClass("wmsDisplayNone");
					$("DIV#left-side").addClass("wmsDisplayNone");
					$("DIV#right-side-wrapper").addClass("wmsDisplayNone");
					$("FOOTER").addClass("wmsDisplayNone");
					// show zoom
					$("DIV#main").addClass("wmsMarginZero").addClass("wmsPresenterZoom");
					// set height to prevent page from being cut-off (dynamic height of primary div * 1.5 zoom modifier)
					$("DIV#main.wmsPresenterZoom").css('cssText', 'min-height: ' + this._originalHeight * 1.5 + 'px !important;');
					// show exit button (on extreme left side)
					$("#wms_presenter_exit_btn").addClass("wmsPresenterExit").prop("title","Exit Presenter View");
					$("#wms_presenter_exit_text").removeClass("wmsDisplayNone");
				}
				ele.data('clickState', !ele.data('clickState'));
			});
		};
	})( jQuery );
	$("#wms_presenter_exit_btn").togglePresenterView();


}); // END OF: (document).ready
