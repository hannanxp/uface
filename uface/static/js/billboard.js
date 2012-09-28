jQuery(function($){
    function _init() {
        _load();
        var pos, x = 0, y = 300;
        $(".module").each(function(){
            x += 100;
            y += 30;
            $(this).dialog({
                position: [x, y]
            });
        });
        
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
    
    _init();
});