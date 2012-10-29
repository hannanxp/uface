jQuery(function($){
    
    function _init() {
        
        // popup dialog
        $(".billboard-content .msg-item").live("click", function(){
            var msg_body = $(this).find(".msg-body").html(),
                msg_id = $(this).find(".msg-id").html(),
                msg_category = $(this).find(".msg-category").html(),
                dialog_cname = 'bb-msg-dialog',
                bbtoken = $("#bb-token").html();
            
            console.log(msg_category);
            //msg_body = $(this).find(".msg-body").html()
                /*
                +
                "<div class='msg-options'>[ <span class='msg-option accept' title='"
                + $(this).find(".msg-id").html() + "'>"
                + "OK, I understand</span> ]"
                + "&nbsp;&nbsp;[ <span class='msg-option delete' title='"
                + $(this).find(".msg-id").html() + "'>"
                + "Delete</span> ]"
                + "</div>";
                */
                
            $("#billboard-message").html(msg_body);
            $("#billboard-message").dialog({
                dialogClass : dialog_cname,
                title: $(this).find(".msg-subject").html(),
                width: 600,
                height: 300,
                buttons: {
                    "Ok, I understand": function() {
                        $.ajax({
                            url: "/bb/acceptmsg/",
                            type: 'POST',
                            data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                            success: function(data) {
                                //console.log(data);
                                //console.log($(".msg-id:contains('"+data.msg_id+"')").parent());
                                $(".msg-id:contains('"+data.msg_id+"')").parent().addClass("archived");
                                $("#billboard-message").dialog( "close" );
                            },
                            dataType: "json"
                        });
                        //$(this).dialog("close");
                    },
                    "Delete": function() {
                        $.ajax({
                            url: "/bb/delmsg/",
                            type: 'POST',
                            data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                            success: function(data) {
                                //console.log(data);
                                //console.log($(".msg-id:contains('"+data.msg_id+"')").parent());
                                $(".msg-id:contains('"+data.msg_id+"')").parent().hide();
                                $("#billboard-message").dialog( "close" );
                            },
                            dataType: "json"
                        });
                        //$(this).dialog("close");
                    },
                }
            });
            
            if (msg_category != 'p') {
                $( '.' + dialog_cname + ' .ui-dialog-buttonpane button:contains("Delete")').attr('disabled', true );
            }
            else {
                $( '.' + dialog_cname + ' .ui-dialog-buttonpane button:contains("Delete")').attr('disabled', false );
            }
            
        });
        
        /*
        // accept message
        $(".msg-options .accept").live("click", function(){
            var msg_id = $(this).attr('title'),
                bbtoken = $("#bb-token").html();
                
            $.ajax({
                url: "/bb/acceptmsg/",
                type: 'POST',
                data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                success: function(data) {
                    //console.log(data);
                    //console.log($(".msg-id:contains('"+data.msg_id+"')").parent());
                    $(".msg-id:contains('"+data.msg_id+"')").parent().addClass("archived");
                    $("#billboard-message").dialog( "close" );
                },
                dataType: "json"
            });
            
        });
        
        // delete message
        $(".msg-options .delete").live("click", function(){
            var msg_id = $(this).attr('title'),
                bbtoken = $("#bb-token").html();
                
            $.ajax({
                url: "/bb/delmsg/",
                type: 'POST',
                data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                success: function(data) {
                    //console.log(data);
                    //console.log($(".msg-id:contains('"+data.msg_id+"')").parent());
                    $(".msg-id:contains('"+data.msg_id+"')").parent().hide();
                    $("#billboard-message").dialog( "close" );
                },
                dataType: "json"
            });
            
        });
        */
        
        $(".bbapp-region").sortable({
            connectWith: ['.bbapp-region'],
            stop: function() { _saveOrder(); }
        }); 
    }
    
    function _saveOrder() {
        var data = "";
        $(".bbapp-region").each(function(index, value){
            var colid = value.id,
                order,
                i,
                modname;
                
            order = $('#' + colid).sortable("toArray");
                
            for (i = 0; i < order.length; ++i) {
                //console.log(index, i, order[i]);
                modname = order[i];
                modname = modname.substring(6);
                data = data + "," + index + ":" + i + ":" + modname;
            }
            
        });
        data = data.substring(1);
        
        // save to the server
        var bbtoken = $("#bb-token").html();
        $.ajax({
            url: "/bb/saveapps/",
            type: 'POST',
            data: {apps: data, csrfmiddlewaretoken: bbtoken},
            success: function(data) {
                //console.log(data);
            },
            dataType: "json"
        });
    }
    
    _init();
});