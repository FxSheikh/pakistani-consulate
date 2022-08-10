$(document).ready(function() {
	$('ul.tabs').tabs();
	$('select').material_select();

	toggle_counter = 1
	night_counter = 1
	console.log("Ready")
	$(".button-collapse").sideNav();

	$(".toggle-flow").on("click", function(){
		if (toggle_counter == 1) {
			$("div").addClass("flow-text");
			toggle_counter = toggle_counter - 1
		} else {
			$("div").removeClass("flow-text");
			toggle_counter +=1

		}
	});

	$(".night-mode").on("click", function(){
		if (night_counter == 1) {
			$("main").addClass("teal darken-4");
			night_counter = night_counter - 1
		} else {
			$("main").removeClass("teal darken-4");
			night_counter +=1

		}
	});



});



