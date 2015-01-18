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

function popup_message(text)
{
    $('#message-drawer .message-text').text(text)
    $('#message-drawer').show();
    $('#message-drawer').fadeTo("fast", 1.0);
    $('#message-drawer').fadeTo(3000, 0, function(){
        $(this).hide();
    });
}

function main() {
    //var parent_url = (window.location != window.parent.location) ? document.referrer: document.location;
    //var target_url = 'http://www.tengmanpinglun.com:8000/comment/' + btoa(parent_url);
    var l = document.location
    var target_url = l.protocol + l.origin + l.pathname
    var pathname = l.pathname

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
            }, 3000);

            if (comment_input.val().length > 140 || comment_input.val().length < 5) {
                popup_message("输入长度要在5-140之间哟小伙伴~");
                return;
            }

            var pageshot = null;
            //pageshot
            $.getScript("/static/js/html2canvas.js", function(){
                var htmlcontent = null;
                if(window.location.protocol != "http")
                    htmlcontent = document.body;
                else
                    htmlcontent = (window.location != window.parent.location) ?window.parent.document.body:document.body;
                html2canvas(htmlcontent, {
                  onrendered: function(canvas) {
                      //pageshot = canvas;
                      pageshot = canvas.toDataURL("image/png");
                        //$.post(last_url, {'comment': comment_input.val(), 'pageshot': pageshot, 'target_url': target_url, 'captcha_key':$('#id_captcha_0').val(),'captcha_value':$('#id_captcha_1').val() })
                        var fdata = new FormData();
                        fdata.append('comment', comment_input.val());
                        fdata.append('pageshot', pageshot);
                        fdata.append('target_url', target_url);
                        fdata.append('captcha_key', $('#id_captcha_0').val());
                        fdata.append('captcha_value', $('#id_captcha_1').val());
                        $.ajax({
                            url: last_url,
                            data: fdata,
                            cache: false,
                            contentType: false,
                            processData: false,
                            type: 'POST',
                        })
                        .fail(function(data){if ( data.responseCode ) console.log( data.responseCode );})
                        .done(function(data) {
                            var badge = $('#comments_count');
                            var count = parseInt(badge.html())+1;
                            badge.html(count);

                            $('#showMsg').html(data);
                            comment_input.val('');
                            btn.button('reset');
                            popup_message("吐槽成功");
                        });
                  },
                  //width: 1024,
                  //height: 768
                });
            });
   
        });
    }

    var nav_buttons = {"nav_comment":"comment_raw", "nav_account":"account_raw", "nav_letter":"letter_raw", "nav_setting":"setting_raw"};
    // TODO 把导航变为ajax形式
    for (nav_id in nav_buttons) {
        $("#" + nav_id).on('click', function(){
            var btn = $(this);

            //FIXME l.protocol
            if ($(this).attr('id') != "nav_comment")
                $('#showMsg').load(l.origin + '/' + nav_buttons[btn.attr('id')]);
            else
            // FIXME 注意这里pathname在当前是comment/xxx，以后就不一定了
                $('#showMsg').load(l.origin + '/ajax' + pathname);

            $('.nav .active').removeClass('active');
            btn.addClass('active');
        });
    }
    
    // TODO 把pagenation都变为ajax形式
    for (pageNavi in $('.pagination li a')) {
        ;
    }
}
            
