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
  var parent_url = (window.location != window.parent.location) ? document.referrer: document.location;
  var target_url = 'http://www.anwcl.com:8000/comment/' + btoa(parent_url);
  //在raw template时启用动态load，在meta template时此load会嵌套加载，所以关闭
  //$('#showMsg').load(target_url);

  $("#submitComment").on('click', function(){
	var posting = $.post(target_url, {'comment': $('#comment').val() });
	posting.done(function(data) {
	  $('#showMsg').html(data);
	});
  });
}