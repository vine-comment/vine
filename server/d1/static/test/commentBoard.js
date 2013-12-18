if (typeof jQuery === "undefined") {
    loadjQuery("//code.jquery.com/jquery-1.8.2.min.js", verifyJQueryCdnLoaded);
} else {
    main();
}

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
    //var target_url = 'http://www.anwcl.com:8000/comment/' + btoa(parent_url);
    var l = document.location
    var target_url = l.protocol + l.origin + l.pathname

    // last_url这里作为资源索引，不直接post到/comment上，而是/comment/<last_url>
    var last_url = target_url.replace(/^.*[\\\/]/, '')
    // 老方法：先load一次target。新方法：直接通过iframeview来load。
    // $('#showMsg').load(target_url);
    var buttonCommentRelations = {"submitCommentTop":"commentTop","submitCommentBottom":"commentBottom"};

    //这里target_url暂未使用，仅用comment
    for (buttonSubmitComment in buttonCommentRelations) {
        $("#" + buttonSubmitComment).on('click', function(){
            var btn = $(this);
            var comment_input = $("#" + buttonCommentRelations[btn.attr('id')]);
            btn.button('loading');
            setTimeout(function () {
                btn.button('reset');
            }, 2000);

            var posting = $.post(last_url, {'comment': comment_input.val(), 'target_url': target_url })
            .fail(function(data){if ( data.responseCode ) console.log( data.responseCode );});
            posting.done(function(data) {
                $('#showMsg').html(data);
                comment_input.val('');
                btn.button('reset');
                $('#message-drawer').show();
                $('#message-drawer').css('opacity', 1);
                $('#message-drawer').fadeTo(3500, 0, function(){
                    $(this).hide();
                });
            });
        });
    }

    // TODO 把pagenation都变为ajax形式
    for (pageNavi in $('.pagination li a')) {
        ;
    }
}
            