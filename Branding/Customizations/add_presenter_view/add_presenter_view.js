$(document).ready(function () {

	/***********************************************
	 ** Add Presenter View (zoom main div; hide all other columns)
	 ***********************************************/
	/*
	 * START: Scale a page using CSS3
	 * @param minWidth {Number} The width of your wrapper or your page's minimum width.
	 * @return {Void}
	 * author of scalePage fxn: http://binarystash.blogspot.com/2013/04/scaling-entire-page-through-css3.html
	 */
	function scalePage(minWidth) {

		//Check parameters
		if (minWidth == "") {
			console.log("minWidth not defined. Exiting");
			return;
		}

		//Do not scale if a touch device is detected.
		if (isTouchDevice()) {
			return;
		}

		//The 'body' tag should generally be the parent element, but hack works better with Canvas
		var parentElem = "#wrapper-container";

		//Wrap content to prevent long vertical scrollbars
		$(parentElem).wrapInner('<div id="resizer-boundary" />');
		$("#resizer-boundary").wrapInner('<div id="resizer-supercontainer" />');

		var boundary = $("#resizer-boundary");
		var superContainer = $("#resizer-supercontainer");

		//Get current dimensions of content
		var winW = $(window).width();
		var docH = $(parentElem).height();

		scalePageNow();
		$(window).resize(scalePageNow);

		//Nested functions

		function scalePageNow() {
			//Defining the width of 'supercontainer' ensures that content will be
			//centered when the window is wider than the original content.
			superContainer.width(minWidth);

			//Get the width of the window
			winW = $(window).width();

			var newWidth = winW / minWidth; //percentage
			var newHeight = (docH * (newWidth * minWidth)) / minWidth; //pixel
			superContainer.css({
				"transform": "scale(" + newWidth + ")",
				"transform-origin": "0 0",
				"-ms-transform": "scale(" + newWidth + ")",
				"-ms-transform-origin": "0 0",
				"-moz-transform": "scale(" + newWidth + ")",
				"-moz-transform-origin": "0 0",
				"-o-transform": "scale(" + newWidth + ")",
				"-o-transform-origin": "0 0",
				"-webkit-transform": "scale(" + newWidth + ")",
				"-webkit-transform-origin": "0 0"
			});
			boundary.css({
				"position": "relative",
				"overflow": "hidden",
				"height": newHeight + "px"
			});
		}

		function isTouchDevice() {
			return !!('ontouchstart' in window || window.navigator.msMaxTouchPoints);
		}
	}

	// END OF FUNCTION: scalePage()

	// Url must match this pattern (Do not display "Presenter View" link on pages that display LTI iframes)
	if (!window.location.href.match(/\/external_tools/ig)) {
		$("NAV#breadcrumbs UL LI").first().before('<div id="wms_presenter_exit_btn" style="float: right;"><div id="wms_presenter_exit_text" class="wmsPresenterRotate wmsDisplayNone">Exit&nbsp;Presenter&nbsp;View</div><a id="wms_presenter_breadcrumb" class="btn-mini" href="#" title="Enable Presenter View"><i class="icon-off"></i> Presenter View</a>&nbsp;&nbsp;</div>');
	}

	// Presenter View: Create custom toggle click state
	(function ($) {
		$.fn.togglePresenterView = function () {
			var ele = this;
			ele.data('clickState', 0);
			ele.click(function () {
				if (ele.data('clickState')) {
					// refresh page
					location.reload();
				}
				else {
					// hide breadcrumb link and page elements
					$("#wms_presenter_breadcrumb").addClass("wmsDisplayNone");
					$("DIV#header").addClass("wmsDisplayNone");
					$("DIV#left-side").addClass("wmsDisplayNone");
					$("DIV#right-side-wrapper").addClass("wmsDisplayNone");
					$("DIV#main").addClass("wmsMarginZero").css("cssText", "padding-left: 25px;max-width: 900px !important;"); // max-width should match value given to scalePage(), below
					// force all images to zoom correctly and avoid cutting off images; requires removing the default style: IMG{max-width:1050px}
					$("IMG").css("cssText", "max-width: 100% !important;");

					// do scale function
					scalePage(900); // set somewhat arbitrary hardcoded minWidth value

					// show exit button (on extreme left side)
					$("#wms_presenter_exit_btn").addClass("wmsPresenterExit").prop("title", "Exit Presenter View");
					$("#wms_presenter_exit_text").removeClass("wmsDisplayNone");
				}
				ele.data('clickState', !ele.data('clickState'));
			});
		};
	})(jQuery);
	$("#wms_presenter_exit_btn").togglePresenterView();


}); // END OF: (document).ready
