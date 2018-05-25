$(document).ready(function(){

    //loadFrame()
    //dumpLogs()
    url = 'http://' + document.domain + ':' + location.port + '/nocontainer'
    var link= document.getElementById('vnc_frame_src'); 
    link.href = url

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
        
        var projectname=   $("input[name='projectname']:checked").val();
        var data = {'projectname': projectname };
        $.ajax({
            type: "POST",
            url: "/run",
            dataType: 'json',
            data: data,
            success: function(response) {
                loadFrame();
            },
            error: function(response) {
                loadFrame();
            }
        });
    })

        $("#delete").click(function() {

        var projectname=   $("input[name='projectname']:checked").val();
        var data = {'projectname': projectname };
        $.ajax({
            type: "POST",
            url: "/delete",
            dataType: 'json',
            data: data,
            success: function(response) {
                loadFrameAfterDelete();
            },
            error: function(response) {
                loadFrameAfterDelete();
            }
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
                console.log("test");
                document.body = response;
                console.log("test2");
                $('#log').append("test2");
            },
        });
    });
    
    $("#clear").click(function() {
        $('#log').html("");
    });
})

function loadFrame() {
    var vnc_port_cookie = document.cookie.match(new RegExp('vnc_port=([^;]+)'));
    var port = !!vnc_port_cookie ? vnc_port_cookie[1] : null;
    url = 'http://' + document.domain + ':' + port + '/vnc_auto.html'
    console.log(url)
    var link= document.getElementById('vnc_frame_src'); //or grab it by tagname etc
    link.href = url
    window.open(url, '_blank');
 
    var ssh_port_cookie = document.cookie.match(new RegExp('ssh_port=([^;]+)'));
    var ssh_port = !!ssh_port_cookie ? ssh_port_cookie[1] : null;
    console.log(ssh_port)
    
    var command= document.getElementById('ssh_command');
    command.innerHTML = "ssh -p " + ssh_port + " root@" + document.domain
    //document.getElementById('vnc_frame').src = url
}

function loadFrameAfterDelete() {
    var command= document.getElementById('ssh_command');
    command.innerHTML = "Container Deleted."
    var link= document.getElementById('vnc_frame_src'); //or grab it by tagname etc
    link.href = 'http://' + document.domain + ':' + location.port + '/nocontainer'

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
