document.addEventListener('DOMContentLoaded', function () {
    if (!window.btoa) window.btoa = base64.encode;
    $('body').append('<div id="vine_comment_iframe"></div>');
    $.support.cors = true;
    $('#vine_comment_iframe').load("http://114.215.113.3:8000/danmu/" + btoa(document.location));
});

/*
var url = document.location.host;
var pathname = window.location.pathname;
console.log(url)
console.log(pathname)
// Special 2: +-
window.btoa = base64.encode;
//$('body').append('<div id="vine_comment_iframe">Loading...</div>');
$.support.cors = true;
$('iframe').attr('src', "http://114.215.113.3:8000/danmu/" + btoa(url));
*/
