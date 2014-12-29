
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
