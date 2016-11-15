$('body').ready(function(){
	set_cover_section_ready(this);
	set_portfolio_section_ready(this);
});

function set_cover_section_ready(obj){
	$(obj).find('#cover').each(function(){
	    $(this).carousel({
	        interval: 5000 //changes the speed
	    });
	});
}


function set_portfolio_section_ready(obj){
	$(obj).find('#portfolio').each(function(){
		var album_image_controller = $(this).find('.album-image-controllers');
		var carousel = $(this).find('#slider');
	    $(carousel).carousel({
			interval: 5000
		});
		$(album_image_controller).click(function(){
		});
	});
}