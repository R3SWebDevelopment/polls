$('body').ready(function(){
	set_drag_n_draw_upload_files_section_ready(this);
});

function set_drag_n_draw_upload_files_section_ready(obj){
	var holder = $(obj).find('#drag-n-draw-upload-files-panel-holder');
	$(holder).each(function(){
		var dropZone = $(holder).find('#drop-zone');
		var uploadForm = $(holder).find('#js-upload-form');
		var url = $(uploadForm).attr('action');
		var csrf = $(uploadForm).find('[name="csrfmiddlewaretoken"]')
		var csrf_value = $(csrf).val();
		$(dropZone).dropzone({
			url: url ,
			parallelUploads: 10 ,
			sending: function(file , xhr , formData){
				formData.append("csrfmiddlewaretoken", csrf_value);
			} ,
			drop: function(){
				$(dropZone).addClass('upload-drop-zone')
			} ,
			createImageThumbnails: false
		})
	});
}