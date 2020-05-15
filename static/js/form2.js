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


				$('#rating5').text(data.rating5).show();
				$('#rating10').text(data.rating10).show();

		});

		event.preventDefault();

	});

});