let dataPoints = {};

/* --- Dashboard parameters ------- */
let justChangedHighlightDuration;
let recentlyChangedHighlightDuration;
let diagnosticCount = 0;
/* --- End dashboard parameters --- */

var valueChangedTimer;
var valueRecentlyChangedTimer;

$(document).ready(function() {
	updateDashboardParameters();
	searchTable()

	var f_sl = 1;
	var f_nm = 1;
	$("#sn").click(function(){
		f_sl *= -1;
		var n = $(this).prevAll().length;
		sortTable(f_sl,n);
	});
	$("#sv").click(function(){
		f_nm *= -1;
		var n = $(this).prevAll().length;
		sortTable(f_nm,n);
	});
	$("#sr").click(function(){
		f_nm *= -1;
		var n = $(this).prevAll().length;
		sortTable(f_nm,n);
	});
	$("#sf").click(function(){
		f_nm *= -1;
		var n = $(this).prevAll().length;
		sortTable(f_nm,n);
	});


	var namespace = '';
	var socket = io(namespace);
	socket.on('vehicle data', function(msg, cb) {
		// console.log(msg);

		if (!msg.hasOwnProperty('command_response')) {
			if (msg.hasOwnProperty('success')) {
				// Using the 'success' property to identify a diagnostic response
				diagnosticCount++;
				let diagnosticName = 'diagnostic_' + diagnosticCount;
				addDiagnosticResponse(diagnosticName, msg);
			} else {
				if (!msg.hasOwnProperty('name')) {
					msg.name = 'Raw-' + msg.bus + '-0x' + msg.id.toString(16);
					msg.value = msg.data;
				}

				if (msg.hasOwnProperty('event')) {
					msg.value = msg.value + ': ' + msg.event
				}

				if (!(msg.name in dataPoints)) {
					dataPoints[msg.name] = {
						current_data: undefined,
						events: {},
						messages_received: 0,
						measurement_type: undefined,
						min: undefined,
						max: undefined,
						last_update_time: undefined,
						average_time_since_update: undefined
					};
				}

				updateDataPoint(dataPoints[msg.name], msg);
				updateDisplay(dataPoints[msg.name]);

				if (cb) {
					cb();
				}
			}
		}
	});
});

function updateDashboardParameters() {
	valueChangedTimer = Number($('#justChangedHighlightDuration').val());
	valueRecentlyChangedTimer = Number($('#recentlyChangedHighlightDuration').val());
}

function saveSettings(e) {
	e.preventDefault();
	updateDashboardParameters();
}

function addToDisplay(msgName) {
	$('<tr/>', {
		id: msgName
	}).appendTo('#log');

	$('<td/>', {
		id: msgName + '_label',
		text: msgName
	}).appendTo('#' + msgName);

	$('<td/>', {
		id: msgName + '_value'
	}).appendTo('#' + msgName);

	$('<td/>', {
		id: msgName + '_num',
		class: 'metric'
	}).appendTo('#' + msgName);

	$('<td/>', {
		id: msgName + '_freq',
		class: 'metric'
	}).appendTo('#' + msgName);
}

function updateDisplay(dataPoint) {
	var msg = dataPoint.current_data

	if ($('#' + msg.name).length <= 0) {
		addToDisplay(msg.name);
	}

	$('#' + msg.name + '_value').text(msg.value);
	highlightCell('#' + msg.name + '_value');

	$('#' + msg.name + '_num').text(dataPoint.messages_received);
	$('#' + msg.name + '_freq').text(Math.ceil(1 / dataPoint.average_time_since_update));
}

function highlightCell(cellId) {
	$(cellId).stop(true);
	$(cellId).css({'background': '#1338F0', 'color': 'white'});
	$(cellId).animate({backgroundColor: '#949494'}, valueChangedTimer, function() {
		$(this).animate({backgroundColor: '#FFFFFF', color: 'black'}, valueRecentlyChangedTimer);
	});
}

function validateSettingsForm() {
	let valid = true;
	let errors = [];

	$('.error').each(function() {
		$(this).text('');
	});

	errors = validateTimerInput($('#justChangedHighlightDuration'), errors);
	errors = validateTimerInput($('#recentlyChangedHighlightDuration'), errors);

	if (errors.length > 0) {
		valid = false;
		errors.forEach(function(e) {
			$('#' + e.id + '_error').text(e.msg);
		});
	}

	return valid;
}

function validateTimerInput(input, errors) {
	let inputVal = input.val();

	if (isNaN(inputVal) || inputVal < 0) {
		errors.push({id: input[0].id, msg: 'Input must be a positive number'});
	}

	return errors;
}

function updateDataPoint(dataPoint, measurement) {
	dataPoint.messages_received++;
	dataPoint.current_data = measurement;
	let update_time = (new Date()).getTime() / 1000;

	if (dataPoint.last_update_time !== undefined) {
		dataPoint.average_time_since_update =
			calculateAverageTimeSinceUpdate(update_time, dataPoint);
	}

	dataPoint.last_update_time = update_time;

	if ('event' in measurement) {
		dataPoint.events[measurement.value] = measurement.event;
	}
}

function calculateAverageTimeSinceUpdate(updateTime, dataPoint) {
	let time_since_update = updateTime - dataPoint.last_update_time;

	return (dataPoint.average_time_since_update === undefined)
		? time_since_update
		: (0.1 * time_since_update) + (0.9 * dataPoint.average_time_since_update);
}

function sortTable(f,n){
	var rows = $('#log tbody  tr').get();

	rows.sort(function(a, b) {

		var A = getVal(a);
		var B = getVal(b);

		if(A < B) {
			return -1*f;
		}
		if(A > B) {
			return 1*f;
		}
		return 0;
	});

	function getVal(elm){
		var v = $(elm).children('td').eq(n).text().toUpperCase();
		if($.isNumeric(v)){
			v = parseInt(v,10);
		}
		return v;
	}

	$.each(rows, function(index, row) {
		$('#log').children('tbody').append(row);
	});
	console.log("jamez test");
}

function searchTable() {
	$("#myInput").on("keyup", function() {
		var value = $(this).val().toLowerCase();
		$("#log tr").filter(function() {
			$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
		});
	});
}

function addDiagnosticResponse(name, message) {
	$('<tr/>', {
		id: name
	}).appendTo('#diagnostic');

	$('<td/>', {
		id: name + '_bus',
		text: message.bus
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_id',
		text: message.id
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_mode',
		text: message.mode
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_pid',
		text: message.pid
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_success',
		text: message.success
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_payload',
		text: message.payload
	}).appendTo('#' + name);

	$('<td/>', {
		id: name + '_value',
		text: message.value
	}).appendTo('#' + name);

	if (message.success == false) {
		$('<td/>', {
			id: name + '_neg_resp_code',
			text: message.negative_response_code
		}).appendTo('#' + name);
	}
}
