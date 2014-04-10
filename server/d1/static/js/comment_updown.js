		function up(id) {
            var onclick = $('#up_comment_'+id).attr('onclick');
            $('#up_comment_'+id).prop('onclick','return false;');
		    $.get("/ajax/up/comment/"+id)
			 .done(function(data){
					if (data == "up-1") {
							popup_message(data);
							var ups = $('#up_comment_'+id).find('span');
							var count = parseInt(ups.text())-1;
							ups.text(count);
							var up_icon = $('#up_comment_'+id).find('i');
							up_icon.prop('class', "fa fa-thumbs-o-up");
					} else if (data == "up+1") {
							popup_message(data);
							var ups = $('#up_comment_'+id).find('span');
							var count = parseInt(ups.text())+1;
							ups.text(count);
							var up_icon = $('#up_comment_'+id).find('i');
							up_icon.prop('class', "fa fa-thumbs-up");
					} else if (data == "down-1,up+1") {
							popup_message(data);
							var downs = $('#down_comment_'+id).find('span');
							var count = parseInt(downs.text())-1;
							downs.text(count);
							var down_icon = $('#down_comment_'+id).find('i');
							down_icon.prop('class', "fa fa-thumbs-o-down fa-flip-horizontal");

							var ups = $('#up_comment_'+id).find('span');
							var count = parseInt(ups.text())+1;
							ups.text(count);
							var up_icon = $('#up_comment_'+id).find('i');
							up_icon.prop('class', "fa fa-thumbs-up");
					}
                    $('#up_comment_'+id).attr('onclick',onclick);//must use attr, not prop
			 });
		};
		function down(id) {
            var onclick = $('#down_comment_'+id).attr('onclick');
            $('#down_comment_'+id).prop('onclick','return false;');
			$.get("/ajax/down/comment/"+id)
			 .done(function(data){
					if (data == "down-1") {
							popup_message(data);
							var downs = $('#down_comment_'+id).find('span');
							var count = parseInt(downs.text())-1;
							downs.text(count);
							var down_icon = $('#down_comment_'+id).find('i');
							down_icon.prop('class', "fa fa-thumbs-o-down fa-flip-horizontal");
					} else if (data == "down+1") {
							popup_message(data);
							var downs = $('#down_comment_'+id).find('span');
							var count = parseInt(downs.text())+1;
							downs.text(count);
							var down_icon = $('#down_comment_'+id).find('i');
							down_icon.prop('class', "fa fa-thumbs-down fa-flip-horizontal");
					} else if (data == "up-1,down+1") {
							popup_message(data);
							var ups = $('#up_comment_'+id).find('span');
							var count = parseInt(ups.text())-1;
							ups.text(count);
							var up_icon = $('#up_comment_'+id).find('i');
							up_icon.prop('class', "fa fa-thumbs-o-up");

							var downs = $('#down_comment_'+id).find('span');
							var count = parseInt(downs.text())+1;
							downs.text(count);
							var down_icon = $('#down_comment_'+id).find('i');
							down_icon.prop('class', "fa fa-thumbs-down fa-flip-horizontal");
					}
                    $('#down_comment_'+id).attr('onclick',onclick);//must use attr, not prop
			 });
		};
