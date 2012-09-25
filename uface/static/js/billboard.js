jQuery(function($){
    function _init() {
        _load();
        setTimeout(_init, 10000); // 10 sec.
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