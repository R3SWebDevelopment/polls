$('body').ready(function(){
	setResponseView(this);
});

function setResponseView(obj){
	$(obj).find('#responsePoll').each(function(){
		var form = this;
		var idField = $(this).find('#id_instanceId');
		var actionField = $(this).find('#id_action');
		var sourceField = $(this).find('#id_source');
		$(this).find('button#send-id').click(function(){
			var id = $(this).data('id');
			var action = $(this).data('action');
			var source = $(this).data('source');
			$(idField).val(id);
			$(actionField).val(action);
			$(sourceField).val(source)
		});
		$(this).find('#poll-controls').each(function(){
			$(this).find('#save').click(function(){
				var url = $(this).data('url');
				$(form).attr('action' , url);
			});
		});	
	});
}