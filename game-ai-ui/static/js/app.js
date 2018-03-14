$(document).ready(function(){

    loadFrame()
    dumpLogs()

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
                loadFrame();
                //dumpLogs();
            },
            async: false
        });
    })

    $("#getlastlog").click(function() {
        $.ajax({
            type: "POST",
            url: "/getLog",
            success: function(response) {
                $('#log').append(response);
                dumpLogs();
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

function loadFrame() {
    var vnc_port_cookie = document.cookie.match(new RegExp('vnc_port=([^;]+)'));
    var port = !!vnc_port_cookie ? vnc_port_cookie[1] : null;
    url = 'http://' + document.domain + ':' + port + '/vnc_auto.html'
    console.log(url)
    document.getElementById('vnc_frame').src = url
}

function dumpLogs() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/getlogs');
    var user_name_cookie = document.cookie.match(new RegExp('userID=([^;]+)'));
    var user_name = !!user_name_cookie ? user_name_cookie[1] : null;
    socket.on(user_name, function(line_received) {
        line_print = '<p>' + line_received + '<p>';
        $('#log').append(line_print);
        document.getElementById("log").scrollTop = document.getElementById("log").scrollHeight;
    });
}
