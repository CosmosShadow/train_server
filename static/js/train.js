$(document).ready(function() {
	var refresh = function() {
		$.get('/data/train.json' + window.location.search, function(status) {
			status = JSON.parse(status)
			if (status.hasOwnProperty('show')){
				Plotly.newPlot('main', status['show']);
			}
		})
	}
	refresh();
	// setInterval(refresh, 10000);
})
