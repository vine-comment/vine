
(function() {
    // Load the script
    var script = document.createElement("SCRIPT");
    script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js';
    script.type = 'text/javascript';
    document.getElementsByTagName("head")[0].appendChild(script);

    // Poll for jQuery to come into existance
    var checkReady = function(callback) {
        if (window.jQuery) {
            callback(jQuery);
        }
        else {
            window.setTimeout(function() { checkReady(callback); }, 100);
        }
    };

    // Start polling...
    checkReady(function($) {
	    var jQuery_anwcl = jQuery.noConflict();
		jQuery_anwcl('body').append('<div id="test"></div>');
		jQuery_anwcl('#test').load("http://www.anwcl.com:8000/static/test/iframe_test.html");
    });
})();

