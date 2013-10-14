if (typeof jQuery === "undefined") {
  loadjQuery("//code.jquery.com/jquery-1.8.2.min.js", verifyJQueryCdnLoaded);
} else {
  main();
}

function verifyJQueryCdnLoaded() {
  if (typeof jQuery === "undefined") {
    loadjQuery("//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js", main);
  } else {
    main();
  }
}

function loadjQuery(url, callback) {
  var script_tag = document.createElement('script');
  script_tag.setAttribute("src", url)
  script_tag.onload = callback; // Run callback once jQuery has loaded
  script_tag.onreadystatechange = function () { // Same thing but for IE... bad for IE 10, it supports all
    if (this.readyState == 'complete' || this.readyState == 'loaded') {callback();}
  }
  script_tag.onerror = function() {
    loadjQuery("http://code.jquery.com/jquery-1.8.2.min.js", main);
  }
  document.getElementsByTagName("head")[0].appendChild(script_tag);
}

function main() {
  $("#special_div_for_anwcl_comment_board #boardButton").on('click', function(){
	if (!$(this).attr('data-toggled') || $(this).attr('data-toggled') == 'off') {
	  $("#special_div_for_anwcl_comment_board").animate({right:'0'});
	  $(this).attr('data-toggled','on');
	  $(this).html(">");
	} else {
	  $("#special_div_for_anwcl_comment_board").animate({right:'-40%'});
	  $(this).attr('data-toggled','off');
	  $(this).html("<");
	}
  });
}