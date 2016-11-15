$('body').ready(function(){
	set_nav_menu_ready(this);
});


function set_nav_menu_ready(obj){
	var nav_menu = $(obj).find('#nav-menu');
	var collapsable_items = $(nav_menu).find('a[data-toggle="collapse"]');
	$(collapsable_items).click(function(event){
		event.preventDefault();
		var target = $(this).data('target');
		target = $(this).parent().find(target + " li");
		if($(this).data('status') == 'closed'){
			$(target).removeClass('hide');
			$(this).data('status' , 'opened');
		}else if($(this).data('status') == 'opened'){
//			$(target).addClass('hide');
			$(this).data('status' , 'closed');
		}
	});
}