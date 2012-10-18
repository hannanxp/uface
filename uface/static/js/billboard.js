jQuery(function($){
    var moduleBox = [];
    
    function _init() {
        _load();
        
        
    }
    
    function _renderDialog() {
        //console.log(moduleBox);
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
                _renderDialog();
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
        var i, msg;
        for (i = 0; i < messages.i.length; ++i) {
            $("#billboard-important")
                .find(".billboard-content")
                .append("<div class='msg-item'>[&bull;] "+ messages.i[i].s +"</div>");
        }
        
        for (i = 0; i < messages.p.length; ++i) {
            $("#billboard-personal")
                .find(".billboard-content")
                .append("<div class='msg-item'>[&bull;] "+ messages.p[i].s +"</div>");
        }
        
        for (i = 0; i < messages.u.length; ++i) {
            $("#billboard-useful")
                .find(".billboard-content")
                .append("<div class='msg-item'>[&bull;] "+ messages.u[i].s +"</div>");
        }
    }
    
    _init();
});