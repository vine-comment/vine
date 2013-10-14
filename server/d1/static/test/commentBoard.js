if (typeof jQuery === "undefined") {
  loadjQuery("//code.jquery.com/jquery-1.8.2.min.js", verifyJQueryCdnLoaded);
} else 
  main();

function verifyJQueryCdnLoaded() {
  if (typeof jQuery === "undefined")
    loadjQuery("script/jquery-1.8.2.js", main);
  else
    main();
}

function loadjQuery(url, callback) {
  var script_tag = document.createElement('script');
  script_tag.setAttribute("src", url)
  script_tag.onload = callback; // Run callback once jQuery has loaded
  script_tag.onreadystatechange = function () { // Same thing but for IE
    if (this.readyState == 'complete' || this.readyState == 'loaded') callback();
  }
  script_tag.onerror = function() {
    loadjQuery("script/jquery-1.8.2.js", main);
  }
  document.getElementsByTagName("head")[0].appendChild(script_tag);
}

function main() {
  $('#showMsg').load('http://www.anwcl.com:8000/comment/');

  $("#submitComment").on('click', function(){
	var posting = $.post("http://www.anwcl.com:8000/comment/", {'comment': $('#comment').val() });
	posting.done(function(data) {
	  $('#showMsg').html(data);
	});
  });
}