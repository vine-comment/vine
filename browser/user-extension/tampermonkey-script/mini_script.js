// ==UserScript==
// @name       try-to-comment
// @namespace  http://www.baidu.com/
// @version    0.2
// @description  3rd party comment plugin
// @match      http://www.baidu.com/*
// @copyright  2012+, You
// @require    http://code.jquery.com/jquery-1.8.2.min.js
// @require    http://www.tengmanpinglun.com/static/js/btoa.js
// @grant      unsafeWindow
// ==/UserScript==

window.btoa = base64.encode;
$('body').append('<div id="vine_comment_iframe"></div>');
$('#vine_comment_iframe').load("http://www.tengmangpinglun.com/iframe/" + btoa(document.location));
