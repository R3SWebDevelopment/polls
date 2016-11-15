$('body').ready(function(){
	set_page_ready(this);
	set_general_view_ready(this);
});


function set_page_ready(obj){
	$(obj).find('[data-toggle="tooltip"]').tooltip();
	$(obj).find('.jump-to-page').click(function(event){
		event.preventDefault();
		var href = $(this).attr('href');
		if(!isNull(href)){
			window.location.href = href;
		}else{
			var url = $(this).data('url');
			if(!isNull(url)){
				window.location.href = url;
			}
		}
	});
}

function isNull(variable){
	if (typeof variable !== typeof undefined && variable !== false) {
		return false
	}
	return true
}


function set_general_view_ready(obj){
	$(obj).find('.datepicker').datepicker({
		format: "yyyy-mm-dd"
	})
	var view_on_modal = $(obj).find('.view-on-modal');
	$(view_on_modal).click(function(event){
		event.preventDefault();
		var height = $(this).data('view_on_modal_height');
		var width = $(this).data('view_on_modal_width');
		var title = $(this).data('view_on_modal_title');
		var target = $(this).data('view_on_modal_target');
		var url = $(this).data('view_on_modal_url');
		var view_on_modal_iframe = $(this).data('view_on_modal_iframe');
		if(view_on_modal_iframe){
			var iframe = $("<iframe src = '" + url + "' frameborder = '0' height = '800' width = '100%' scrolling = 'auto'></iframe>");
			$(target).find('.modal-body').html('').append(iframe);
			$(target).modal()
		}else{
			$(target).find('.modal-body').load(url , function(response){
				$(target).modal()
			})
		}
	});
}