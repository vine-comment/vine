
/*
document.addEventListener('DOMContentLoaded', function () {
	if (!window.btoa) window.btoa = base64.encode;
	$('body').append('<div id="vine_comment_iframe"></div>');
	$.support.cors = true;
	$('#vine_comment_iframe').load("http://www.anwcl.com/comment_raw/" + btoa(document.location));
});
*/


//using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

chrome.tabs.getSelected(null,function(tab) {
    var tablink = tab.url;
    // Special 2: +-
	window.btoa = base64.encode;
	//$('body').append('<div id="vine_comment_iframe">Loading...</div>');
	$.support.cors = true;
	$('body iframe').attr('src', "http://www.tengmanpinglun.com/danmu/" + btoa(tablink));
});

  chrome.tabs.captureVisibleTab(function (img) {
    // $('body img').attr('src', image_url);
    console.log(img);
    var xhr = new XMLHttpRequest(), formData = new FormData();
    formData.append("docfile", img);
    //xhr.open("POST", "http://www.tengmanpinglun.com/document/upload", true);
    xhr.open("POST", "http://127.0.0.1:8000/document/upload", true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        // JSON.parse does not evaluate the attacker's scripts.
        var resp = xhr.responseText;
        console.log(resp);
      }
    }
    xhr.send(formData);
  });
