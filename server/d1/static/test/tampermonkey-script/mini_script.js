// ==UserScript==
// @name       try-to-comment
// @namespace  http://use.i.E.your.homepage/
// @version    0.1
// @description  enter something useful
// @match      http://www.anwcl.com
// @copyright  2012+, You
// @require    http://code.jquery.com/jquery-1.8.2.min.js
// @grant      unsafeWindow
// ==/UserScript==

$('body').append('<div id="test"></div>');
$('#test').load("http://www.anwcl.com/test/test_only_div.html");

// Use any event to append the code
$(document).ready(function() 
{
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = '//' + 'www.anwcl.com/test/commentBoard.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
});
