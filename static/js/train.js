$(document).ready(function() {
	waitingDialog.show('loading data...');
	var refresh = function() {
		$.get('/data/train.json' + window.location.search, function(status) {
			status = JSON.parse(status)
			if (status.hasOwnProperty('show')){
				Plotly.newPlot('main', status['show']);
			}
			waitingDialog.hide();
		})
	}
	refresh();
	// setInterval(refresh, 60);
})
