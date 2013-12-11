// ==UserScript==
// @name       try-to-comment
// @namespace  http://www.anwcl.com/
// @version    0.2
// @description  3rd party comment plugin
// @match      http://www.anwcl.com/contact.html
// @exclude    http://www.anwcl.com:8000/*
// @copyright  2012+, You
// @require    http://code.jquery.com/jquery-1.8.2.min.js
// @grant      unsafeWindow
// ==/UserScript==

$('body').append('<div id="vine_comment_iframe"></div>');
$('#vine_comment_iframe').load("http://www.anwcl.com:8000/iframe/" + btoa(document.location));
