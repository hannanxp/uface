jQuery(function($){
    
    function _init() {
        
        $(".billboard-content .msg-item").live("click", function(){
            var msg_body;
            
            msg_body = $(this).find(".msg-body").html() +
                "<div class='msg-options'>[ <span class='msg-option accept' title='"
                + $(this).find(".msg-id").html() + "'>"
                + "OK, I understand</span> ]</div>";
            $("#billboard-message").html(msg_body);
            $("#billboard-message").dialog();
            $("#billboard-message").dialog('option', 'title', $(this).find(".msg-subject").html());
        });
        
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