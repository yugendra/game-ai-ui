$(document).ready(function(){
    $.ajax({
            type: "POST",
            url: "/getFile",
            success: function(response) {
                document.getElementById("file").value = response;   
            }
    });
    
    
    $("#save").click(function() {
        var code = $("#file").val();
        var data = {'data': code};
        console.log(data)
        $.ajax({
        type: "POST",
        url: "/saveFile",
        dataType: 'json',
        data: data,
        encode: true
      });
    });
    
    $("#run").click(function() {
        $.ajax({
            type: "POST",
            url: "/run",
            success: function(response) {
                var info_channel_cookie = document.cookie.match(new RegExp('info_channel=([^;]+)'));
                var port = !!info_channel_cookie ? info_channel_cookie[1] : null;
                url = 'http://' + document.domain + ':' + port
                window.open(url);
            }
        });
    })
    
    $("#user1").click(function() {
        var data = {'user': 'user1'}
        $.ajax({
            type: "POST",
            url: "/login",
            dataType: 'json',
            data: data,
            success: function(response) {
                console.log("test")
                console.log(response)
                document.body = response;
            }
        });
    });
})
