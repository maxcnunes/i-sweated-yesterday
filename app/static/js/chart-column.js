/*
 * data_items variable must be declared and filled before call this js file
 */
 if(typeof data_items === 'undefined'){
    alert('Response data not defined');
 } else {
    // Load the Visualization API and the ColumnChart package.
    google.load('visualization', '1', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);

    // Callback that creates and populates a data table, 
    // instantiates the pie chart, passes in the data and
    // draws it.
    function drawChart() {
        // Create our data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'User');
        data.addColumn('number', 'Total exercises');
        data.addRows(data_items);

        // Set chart options
        var options = { 
                legend: 'none', 
                vAxis: {baseline: 0},
                colors: ['#A0D100']
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.ColumnChart(document.getElementById('chart'));
        chart.draw(data, options);
    }
}