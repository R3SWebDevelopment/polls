$('body').ready(function(){
	set_upload_image_section_ready(this);
});

function set_upload_image_section_ready(obj){
	var upload_image_section = $(obj).find('#upload-image-section');
	$(upload_image_section).each(function(){
		$(this).submit(function(event){
			event.preventDefault();
			var formData = new FormData($(this)[0]);
			var url = $(this).attr('action');
//			var target = $(this).parents('div#item_imagery_list');
			$.ajax({
			url: url ,
			type: 'POST',
			data: formData,
			async: false,
			cache: false,
			contentType: false,
			processData: false,
			success: function (returndata) {
					alert(returndata)
				} ,
			beforeSend: function(){

				} ,
			error: function(){
				alert("An error occurred, please try again,")				
				}
			});

			return false;
		});
	});
}