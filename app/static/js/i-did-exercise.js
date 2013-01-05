$(function() {

	// set value to span exercise date
	$('#date-selected').text($('#date_exercise').val());

    $('#datepicker').datepicker({
        'dateFormat': 'yy/mm/dd',
    	'onSelect': function(dateText, inst) { 
    		$('#date-selected').text(dateText);
    		$('#date_exercise').val(dateText);
    		$(this).slideToggle();
    	} 
    }).hide();

    $('.bt-select-date').click(function (e) {
    	$('#datepicker').slideToggle();
    	e.preventDefault();
    });


    $('input:radio', '#date_exercise_type').change(prepare_select_date);

    // prepare button and calendar
    prepare_select_date();
});

function get_yesterday () {
	// today
	var date_exercise = new Date();
    // yesterday
	date_exercise.setDate(date_exercise.getDate()-1);
    // formated date
	return $.datepicker.formatDate('yy/mm/dd', date_exercise);
}

function prepare_select_date(){
    var yesterday = get_yesterday();
    
    var selected_field = $('input:radio:checked', '#date_exercise_type');
    if (selected_field.is('[value="another_day"]')) {
        $('#datepicker').datepicker('setDate', yesterday);
        $('.bt-select-date').show();
    } else {
        $('.bt-select-date').hide();
        $('#datepicker').slideUp();

        $('#date-selected').text(yesterday);
        $('#date_exercise').val(yesterday);
    }
}