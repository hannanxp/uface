jQuery(function($){
    function _init() {
        _load();
        var pos,
            x = 0,
            y = 300,
            seth = false;
            h = y;
        $(".module").each(function(){
            seth = true;
            x += 100;
            y += 30;
            h += $(this).height() + 110;
            console.log(h);
            $(this).dialog({
                position: [x, y],
                open: function(event, ui) { 
                    $(this).parent().children().children('.ui-dialog-titlebar-close').hide();
                },
                dragStop: function(event, ui) {
                    _changePos($(this).attr('id'), ui.position);
                }

            });
        });
        if (seth) {
            $("body").height(h);
        }
        
    }
    
    function _load() {
        $.ajax({
            url: "/bb/load/",
            success: function(data) {
                console.log(data);
                },
            dataType: "json"
        });

    }
    
    function _changePos(id, pos) {
        console.log(id, pos);
    }
    
    _init();
});