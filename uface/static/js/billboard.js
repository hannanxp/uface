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
    
    function _load() {
        $.ajax({
            url: "/bb/load/",
            success: function(data) {
                console.log(data);
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
                console.log(data);
            },
            dataType: "json"
        });
    }
    
    _init();
});