$('body').ready(function(){
	set_sidebar_section_ready(this);
});

function set_sidebar_section_ready(obj){
	var menu_toggle = $(obj).find("#menu-toggle");
	var fullsize_page = $(menu_toggle).parents('.fullsize-page').first();
	var sidebar = $(obj).find('#wrapper');
	$(sidebar).each(function(){
		if($(this).hasClass('toggled')){
			$(fullsize_page).removeClass('sidebar_opened');
		}else{
			$(this).toggleClass('toggled').each(function(){
				$(fullsize_page).removeClass('sidebar_opened');
//				$(fullsize_page).addClass('sidebar_opened');	
			});
			
		}
	});
	$(menu_toggle).click(function(e) {
	    e.preventDefault();
	    $(sidebar).toggleClass("toggled" , function(){
		}).each(function(){
			if($(this).hasClass('toggled')){
				$(fullsize_page).removeClass('sidebar_opened');
			}else{
				$(fullsize_page).addClass('sidebar_opened');
			}			
		});
	});
}