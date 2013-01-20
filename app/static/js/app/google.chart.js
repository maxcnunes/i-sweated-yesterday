
define('google.chart', ['goog!visualization,1,packages:[corechart]'], function () {

	// Private members
	var 
		dataItems = null,
		chartType = '',
		chart_container = document.getElementById('chart'),

		setDataItems = function (data) {
			 if(typeof dataItems === 'undefined'){
			 	return false; // Response data not defined
			 } else {
			 	dataItems = data;
			 	return true; // Response data defined
			 }
		},

		setChartType = function (type) {
			 if(type != 'column' && type != 'line'){
			 	return false;
			 } else {
			 	chartType = type;
			 	return true;
			 }
		},

		render = function (data, type) {
			
			if(!setDataItems(data)){
				return alert('Response data not defined');
			}

			if(!setChartType(type)){
				return alert('Chart type is not valid');
			}

	        drawVisualization();
	    },

	    getDataTable = function() {
	    	// Create our data table.
	        var dataTable = new google.visualization.DataTable();
	        dataTable.addColumn('string', 'User');
	        dataTable.addColumn('number', 'Total exercises');
	        dataTable.addRows(dataItems);

	        return dataTable;
	    },

	    drawVisualization = function () {
			var dataTable = getDataTable(dataItems);	        

	        // Set chart options
	        var options = getChartOptionsByType();

	        // Instantiate and draw our chart, passing in some options.
	        var chart = getChartByType();
	        chart.draw(dataTable, options);
	    },

	    getChartOptionsByType = function () {
			var options = {};

			if(chartType == 'line'){
				options = { 
	                pointSize: 5,
	                colors: ['#A0D100']
	        	};
			} else if(chartType == 'column'){
				options = { 
	                legend: 'none', 
	                vAxis: {baseline: 0},
	                colors: ['#A0D100']
	        	};
			}
	        
	        return options;
	    },

	    getChartByType = function () {
			var chart = null;

			if(chartType == 'line'){
				chart = new google.visualization.LineChart(chart_container);
			} else if(chartType == 'column'){
				chart = new google.visualization.ColumnChart(chart_container);
			}
	        
	        return chart;
	    };

    // Public members
	return {

		render: render
	};
});