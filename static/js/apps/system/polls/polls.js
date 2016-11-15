$('body').ready(function(){
	setResponseView(this);
	viewOnly(this);
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

function viewOnly(obj){
	var form = $(obj).find('form.viewOnly');
	var poll_controls = $(obj).find('#poll-controls');
	$(poll_controls).hide();
	$(form).each(function(){
		var input = $(this).find('input , textarea , button');
		input = $(input).not('#commit , #save , #goBack');
		$(input).attr('readonly', true).attr('disabled', 'disabled');
	});
}