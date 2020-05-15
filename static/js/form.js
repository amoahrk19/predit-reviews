$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				text : $('#txt').val(),
			},
			type : 'POST',
			url : '/process',
		})
		.done(function(data) {


				$('#rt5').val(data.rating5);
				$('#rt10').val(data.rating10);

		});

		event.preventDefault();

	});

});