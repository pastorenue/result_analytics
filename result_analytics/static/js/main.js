
  $("document").ready(function() {
  	if (screen.width <= 768) {
  		$("#collapse_fixed").removeClass("hide-nav");
  		$("#main_fixed").addClass("hide-nav");
  		$("#desktop_more").addClass("hide-nav");
  		$("#mobile_more").removeClass("hide-nav");
  		$("#left_nav").addClass("hide-nav");
  	}
  });