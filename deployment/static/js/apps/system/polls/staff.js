$('body').ready(function(){
	setSelectMemberSection(this);
});

function setSelectMemberSection(obj){
	var filter = $(obj).find('#filter');
	var selectMember = $(obj).find('.select-member');
	var form = $(obj).find('form#select-members');
	$(selectMember).each(function(){
		var rows = $(this).find('tbody > tr');
		$(rows).each(function(){
			$(this).css({
				'cursor' : 'pointer'
			});
		}).click(function(){
			if($(this).hasClass('info')){
				$(this).removeClass('info');
			}else{
				$(this).addClass('info');
			}
		});
	});
	$(form).submit(function(){
		var selectedMembers = $(this).find('input#members');
		var selectedRows = $(selectMember).find('tbody > tr.info');
		var members = "";
		$(selectedRows).each(function(){
			var val = $(this).data('id') + ",";
			members += val;
		});
		$(selectedMembers).val(members);
	});
	$(filter).change(function(){
		$(selectMember).find('tbody > tr').show();
		if($(filter).val() != '-1'){
			$(selectMember).find('tbody > tr').not('[data-filter~="' + $(filter).val() + '"]').hide();
		}
	});
}