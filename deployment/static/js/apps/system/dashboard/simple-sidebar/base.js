$('body').ready(function(){
	set_sidebar_section_ready(this);
});

function set_sidebar_section_ready(obj){
	var menu_toggle = $(obj).find("#menu-toggle");
	var sidebar = $(obj).find('#wrapper');
	$(menu_toggle).click(function(e) {
	    e.preventDefault();
	    $(sidebar).toggleClass("toggled" , function(){
		});
	});
}