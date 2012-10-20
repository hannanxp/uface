jQuery(function($){
    var moduleBox = [];
    
    function _init() {
        _load();
        _goPortlets();
    }
    
    function _goPortlets() {
        $(".bbapp-region").sortable({
            connectWith: ['.bbapp-region'],
            stop: function() { _saveOrder(); }
        }); 
    }
    
    function _saveOrder() {
        
    }
    
    
    function _renderDialog() {
        //console.log(moduleBox);
        /*
        var pos,
            x = 0,
            y = 300,
            seth = false,
            box,
            h = y;
            
        $(".module").each(function(){
            seth = true;
            box = _getBoxData($(this).attr('id'));
            
            if (box) {
                x = box.posx;
                y = box.posy;
            }
            else {
                x += 100;
                y += 30;
            }
            h += $(this).height() + 110;
            
            $(this).dialog({
                position: [x, y],
                open: function(event, ui) { 
                    $(this).parent().children().children('.ui-dialog-titlebar-close').hide();
                },
                dragStop: function(event, ui) {
                    _chpos($(this).attr('id'), ui.position);
                }

            });
        });
        if (seth) {
            $("body").height(h);
        }
        */
    }
    
    function _getBoxData(id) {
        var i;
        for (i = 0; i < moduleBox.length; ++i) {
            //console.log(jsbox[i].modname);
            if (moduleBox[i].modname == id) {
                return moduleBox[i];
            }
        }
        return false
    }
    
    function _load() {
        $.ajax({
            url: "/bb/load/",
            success: function(data) {
                moduleBox = data.jsbox;
                //_renderDialog();
                _renderBillboard(data.messages);
            },
            dataType: "json"
        });

    }
    
    function _chpos(id, pos) {
        //console.log(id, pos);
        var bbtoken = $("#bb-token").html();
        $.ajax({
            url: "/bb/chpos/",
            type: 'POST',
            data: {modname:id, posx: pos.left, posy: pos.top, csrfmiddlewaretoken: bbtoken},
            success: function(data) {
                //console.log(data);
            },
            dataType: "json"
        });
    }
    
    function _renderBillboard(messages) {
        //console.log(messages);
        var i, msgs, msg_subject, msg_body, archived ;
        
        for (var cat in messages) {
            if (messages.hasOwnProperty(cat)) {
                //console.log(cat, messages[cat]);
                msgs = messages[cat];
                for (i = 0; i < msgs.length; ++i) {
                    if (msgs[i].a == 1) {
                        archived = "archived";
                    }
                    else {
                        archived = "";
                    }
                    $("#billboard-" + cat).find(".billboard-content")
                        .append("<div class='msg-item "+ archived +"'>[&bull;] "
                                + "<span class='msg-subject'>"+ msgs[i].s +"</span>"
                                + "<span class='msg-body'>"+ msgs[i].b +"</span>"
                                + "<span class='msg-id'>"+ msgs[i].id +"</span>"
                                + "</div>");
                }
            }
         }
        
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
        
    }
    
    
    
    _init();
});