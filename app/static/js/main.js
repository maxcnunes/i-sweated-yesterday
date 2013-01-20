
/*
 * RequireJS Configuration
 */

requirejs.config({
	waitSeconds : 10,
	baseUrl: '/static/js',
    paths: {

    	// libs
        'jquery': 'libs/jquery-1.8.3.min',
        'jquery.ui': 'libs/jquery-ui-1.9.2.custom.min',
		
		// plugins requirejs        
        'async' : 'libs/requirejs/async',
        'goog' : 'libs/requirejs/goog',
        'propertyParser' : 'libs/requirejs/propertyParser',

        // app
        'google.chart': 'app/google.chart',
        'i.did.exercise': 'app/i.did.exercise'
    }
});
