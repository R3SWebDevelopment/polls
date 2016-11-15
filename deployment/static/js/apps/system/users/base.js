$('body').ready(function(){
	userControlSection(this);
});

function userControlSection(obj){
	var userControl = $(obj).find('#user-control');
	$(userControl).each(function(){
		var firstName = $(this).find('#firstName');
		$(firstName).blur(function(){
			if($(this).val().trim().length == 0){
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-success').addClass('has-error');
					$(this).find('#firstNameError').removeClass('hide');
					$(this).find('.glyphicon-ok').addClass('hide');
					$(this).find('.glyphicon-remove').removeClass('hide');
				});
			}else{
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-error').addClass('has-success');
					$(this).find('#firstNameError').addClass('hide');
					$(this).find('.glyphicon-ok').removeClass('hide');
					$(this).find('.glyphicon-remove').addClass('hide');
				});
			}
		});
		var lastName = $(this).find('#lastName');
		$(lastName).blur(function(){
			if($(this).val().trim().length == 0){
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-success').addClass('has-error');
					$(this).find('#lastNameError').removeClass('hide');
					$(this).find('.glyphicon-ok').addClass('hide');
					$(this).find('.glyphicon-remove').removeClass('hide');
				});
			}else{
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-error').addClass('has-success');
					$(this).find('#lastNameError').addClass('hide');
					$(this).find('.glyphicon-ok').removeClass('hide');
					$(this).find('.glyphicon-remove').addClass('hide');
				});
			}
		});
		var username = $(this).find('#username');
		$(username).blur(function(){
			if($(this).val().trim().length == 0){
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-success').addClass('has-error');
					$(this).find('#usernameError').removeClass('hide');
					$(this).find('#usernameExistsError').addClass('hide');
					$(this).find('.glyphicon-ok').addClass('hide');
					$(this).find('.glyphicon-remove').removeClass('hide');
				});
			}else{
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-error').addClass('has-success');
					$(this).find('#usernameError').addClass('hide');
					$(this).find('#usernameExistsError').addClass('hide');
					$(this).find('.glyphicon-ok').removeClass('hide');
					$(this).find('.glyphicon-remove').addClass('hide');
				});
				var url = $(this).data('url');
				$.getJSON(url , {
					'username' : decodeURIComponent($(this).val())
				} , function(json) {
					if(json.success){
						if(json.data.exists){
							$(username).parents('div.form-group').each(function(){
								$(this).removeClass('has-success').addClass('has-error');
								$(this).find('#usernameError').addClass('hide');
								$(this).find('#usernameExistsError').removeClass('hide');
								$(this).find('.glyphicon-ok').addClass('hide');
								$(this).find('.glyphicon-remove').removeClass('hide');
							});
						}else{
							$(username).parents('div.form-group').each(function(){
								$(this).removeClass('has-error').addClass('has-success');
								$(this).find('#usernameError').addClass('hide');
								$(this).find('#usernameExistsError').addClass('hide');
								$(this).find('.glyphicon-ok').removeClass('hide');
								$(this).find('.glyphicon-remove').addClass('hide');
							});
						}
					}else{
						
					}
				});
			}
		});
		var email = $(this).find('#email');
		$(email).blur(function(){
			if($(this).val().trim().length == 0){
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-success').addClass('has-error');
					$(this).find('#emailError').removeClass('hide');
					$(this).find('#emailExistsError').addClass('hide');
					$(this).find('.glyphicon-ok').addClass('hide');
					$(this).find('.glyphicon-remove').removeClass('hide');
				});
			}else{
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-error').addClass('has-success');
					$(this).find('#emailError').addClass('hide');
					$(this).find('#emailExistsError').addClass('hide');
					$(this).find('.glyphicon-ok').removeClass('hide');
					$(this).find('.glyphicon-remove').addClass('hide');
				});
				var currentEmail = $(this).data('value');
				if(currentEmail == undefined || (currentEmail != undefined && currentEmail != $(this).val() )){
					var url = $(this).data('url');
					$.getJSON(url , {
						'email' : decodeURIComponent($(this).val())
					} , function(json) {
						if(json.success){
							if(json.data.exists){
								$(email).parents('div.form-group').each(function(){
									$(this).removeClass('has-success').addClass('has-error');
									$(this).find('#emailError').addClass('hide');
									$(this).find('#emailExistsError').removeClass('hide');
									$(this).find('.glyphicon-ok').addClass('hide');
									$(this).find('.glyphicon-remove').removeClass('hide');
								});
							}else{
								$(username).parents('div.form-group').each(function(){
									$(this).removeClass('has-error').addClass('has-success');
									$(this).find('#emailError').addClass('hide');
									$(this).find('#emailExistsError').addClass('hide');
									$(this).find('.glyphicon-ok').removeClass('hide');
									$(this).find('.glyphicon-remove').addClass('hide');
								});
							}
						}else{

						}
					});	
				}else{
					
				}
			}
		});
		var confirmEmail = $(this).find('#confirmEmail');
		$(confirmEmail).blur(function(){
			if($(this).val().trim().length == 0){
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-success').addClass('has-error');
					$(this).find('#confirmEmailError').removeClass('hide');
					$(this).find('#confirmedEmailError').addClass('hide');
					$(this).find('.glyphicon-ok').addClass('hide');
					$(this).find('.glyphicon-remove').removeClass('hide');
				});
			}else{
				if($(email)){
					
				}
				$(this).parents('div.form-group').each(function(){
					$(this).removeClass('has-error').addClass('has-success');
					$(this).find('#confirmEmailError').addClass('hide');
					$(this).find('#confirmedEmailError').addClass('hide');
					$(this).find('.glyphicon-ok').removeClass('hide');
					$(this).find('.glyphicon-remove').addClass('hide');
				});
			}
		});
		///aa
	});
}