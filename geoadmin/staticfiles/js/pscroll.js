(function($) {
	"use strict";

	// For APP-SIDEBAR
	if (document.querySelector('.app-sidebar')) {
		const ps = new PerfectScrollbar('.app-sidebar', {
		  useBothWheelAxes:true,
		  suppressScrollX:true,
		});
	}

	// For Header Message dropdown
	if (document.querySelector('.message-menu')) {
		const ps2 = new PerfectScrollbar('.message-menu', {
			useBothWheelAxes:true,
			suppressScrollX:true,
		});
	}

	// For Header Notification dropdown
	if (document.querySelector('.notifications-menu')) {
		const ps3 = new PerfectScrollbar('.notifications-menu', {
		useBothWheelAxes:true,
		suppressScrollX:true,
		});
	}
	
	// For Header Cart dropdown
	/*
	if (document.querySelector('.cart-menu')) {
		const ps4 = new PerfectScrollbar('.cart-menu', {
		useBothWheelAxes:true,
		suppressScrollX:true,
		});
	}
	*/
})(jQuery);