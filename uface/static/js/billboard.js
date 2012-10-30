jQuery(function($){
    
    function _init() {
        
        // popup dialog
        $(".billboard-content .msg-item").live("click", function(){
            var msg_body,
                msg_id = $(this).find(".msg-id").html(),
                msg_category = $(this).find(".msg-category").html(),
                msg_sender = $(this).find(".msg-sender").html(),
                msg_recipient = $(this).find(".msg-recipient").html(),
                msg_sent_at = $(this).find(".msg-send-at").html(),
                dialog_cname = 'bb-msg-dialog',
                bbtoken = $("#bb-token").html();
                
            // set as read
            $.ajax({
                url: "/bb/readmsg/",
                type: 'POST',
                data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                success: function(data) {
                    $("#msg-item-"+data.msg_id).removeClass("un-read");
                },
                dataType: "json"
            });
            
            msg_body = "<p class='msg-sender-sent-header'><b>"+msg_sender+"</b> &raquo; "+msg_recipient+" | "+msg_sent_at+"</p>";
            msg_body += $(this).find(".msg-body").html();
                
            $("#billboard-message").html(msg_body);
            $("#billboard-message").dialog({
                dialogClass : dialog_cname,
                title: $(this).find(".msg-subject").html(),
                width: 600,
                height: 350,
                buttons: {
                    "Ok, I understand": function() {
                        $.ajax({
                            url: "/bb/acceptmsg/",
                            type: 'POST',
                            data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                            success: function(data) {
                                $("#msg-item-"+data.msg_id).addClass("archived");
                                $("#billboard-message").dialog( "close" );
                            },
                            dataType: "json"
                        });
                        
                    },
                    "Delete": function() {
                        $.ajax({
                            url: "/bb/delmsg/",
                            type: 'POST',
                            data: {msg_id:msg_id, csrfmiddlewaretoken: bbtoken},
                            success: function(data) {
                                $("#msg-item-"+data.msg_id).addClass("archived");
                                $("#billboard-message").dialog( "close" );
                            },
                            dataType: "json"
                        });
                        
                    },
                    "Reply": function() {
                        $(this).dialog("close");
                    }
                }
            });
            
            if (msg_category != 'p') {
                $( '.' + dialog_cname + ' .ui-dialog-buttonpane button:contains("Delete")').attr('disabled', true );
            }
            else {
                $( '.' + dialog_cname + ' .ui-dialog-buttonpane button:contains("Delete")').attr('disabled', false );
            }
            
        });
        
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