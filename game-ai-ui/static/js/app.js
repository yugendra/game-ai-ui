$(document).ready(function(){

    //loadFrame()
    //dumpLogs()
    url = 'http://' + document.domain + ':' + location.port + '/nocontainer'
    var link= document.getElementById('vnc_frame_src');
    link.href = url

        $.ajax({
            type: "POST",
            url: "/getsavedfile",
            success: function(response) {
                $('#file').append(response);
                //dumpLogs();
            }
        });

    $(function () {
    $('#projectname input[type=radio]').change(function(){
      alert ( "Please save your file or remove previous container to launch new project" )
      if ( $(this).val() == "pacman" ){
          $('#log').html("If previous container is running Please remove it first to launch new pacman game.");
          $('#file').html("Pacman code can be found on the given link        >>> git clone https://github.com/golucky5/pacman.git");}
      else if ( $(this).val() == "antivirus" ){
          $('#log').html("If previous container is running Please remove it first to launch antivirus project.");
          $('#file').html("Go to jupyter notebook to modify code.");

      }
      else if ( $(this).val() == "speechrecognition" ){
          $('#log').html("If previous container is running Please remove it first to launch speechrecognition project.");
          $('#file').html("Go to jupyter notebook to modify code.");

      }
      else if ( $(this).val() == "composer" ){
          $('#log').html("If previous container is running Please remove it first to launch composer project.");
          $('#file').html("Go to jupyter notebook to modify code.");

      }
      else if ( $(this).val() == "stockprediction" ){
          $('#log').html("If previous container is running Please remove it first to launch stock_prediction project.");
          $('#file').html("Go to jupyter notebook to modify code.");

      }



      })
    }) ;



    $("#save").click(function() {
        var code = $("#file").text();
        var data = {'data': code};
        console.log(data);
        jQuery('#run_btn_script').attr('disabled',false);
        $.ajax({
        type: "POST",
        url: "/saveFile",
        dataType: 'json',
        data: data,
        encode: true
      });
    });

    $("#run").click(function() {
        var code = $("#file").text();
        var data = {'data': code};
        console.log(data);
        jQuery('#run_btn_script').attr('disabled',false);
        $.ajax({
        type: "POST",
        url: "/saveFile",
        dataType: 'json',
        data: data,
        encode: true
        });

        var code = $("#file").val();
        var projectname=   $("input[name='projectname']:checked").val();
        var data = {'projectname': projectname, 'data': code };
        console.log(data)
        $.ajax({
            type: "POST",
            url: "/run",
            dataType: 'json',
            data: data,
            success: function(response) {
                loadFrame(projectname);
                console.log(response)
                $.ajax({
            type: "POST",
            url: "/getcontainerLog",
            success: function(response) {
                $('#log').append(response);
                //dumpLogs();
            }
        });

            },
            error: function(response) {
                loadFrame(projectname);
                $.ajax({
            type: "POST",
            url: "/getcontainerLog",
            success: function(response) {
                $('#log').html("");
                $('#log').append(response);
                //dumpLogs();
            }
        });



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
            url: "/getcontainerLog",
            success: function(response) {
                $('#log').append(response);
                //dumpLogs();
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
   }) ;



    //DJ Code for
    //enableTab('file');
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/script_exec');
    socket.on('showscript_response', function(response) {
      jQuery('input:radio[name=projectname]:checked').siblings('label').after(jQuery('#files_div'));
      jQuery('#filetree').html(response.content);
      jQuery("#filetree").jstree().bind("select_node.jstree", function (e, data) {
        jQuery('#fileExecutable').val(data.node.data.executable);
        socket.emit('showscript_event',data.node.data.path);
      });
      jQuery('#files_div').show();

    });
    socket.on('scriptcontent_response', function(msg) {
        jQuery('#file').html(msg.data);
        jQuery('#run_btn_script').addClass('hidden');
        //if(jQuery('#fileExecutable').val()==1){
            jQuery('#run_btn_script').removeClass('hidden');
            jQuery('#run_btn_script').text('Run Script');
            jQuery('#run_btn_script').data('filepath',msg.filePath);
            jQuery('#save').removeClass('hidden');
        //}
        jQuery('#filePath').val(msg.filePath);
    });
    jQuery(document).on('click','#run_btn_script',function(){
        socket.emit('runscript_event',{'filePath':jQuery('#filePath').val(),'projectname':jQuery('input:radio[name=projectname]:checked').val()});
        //jQuery('#run_btn_script').text('Running...');
       //dumpLogs();
    });
    socket.on('contentlog_response',function(response){
      jQuery('#log').html(response.content);
    })
    $(document).on('DOMSubtreeModified','#file', function() {
      if(!jQuery('#run_btn_script').hasClass('hidden')){
        jQuery('#run_btn_script').attr('disabled',true);
        jQuery('#save').attr('disabled',false);
      }
    });

    //DJ END 15 June 2018
})

function loadFrame(projectname) {
    console.log(projectname)
    var vnc_port_cookie = document.cookie.match(new RegExp('vnc_port=([^;]+)'));
    var port = !!vnc_port_cookie ? vnc_port_cookie[1] : null;
    if (projectname == "R") {
       console.log("R url")
       url = 'http://' + document.domain + ':' + port + '/vnc_auto.html'
    }
    else if (projectname == "pacman") {
       console.log("pacman url")
       url = 'http://' + document.domain + ':' + port
    }
    else if (projectname == "antivirus") {
       console.log("antivirus url")
       url = 'http://' + document.domain + ':' + port + '/tree?'
    }
    else if (projectname == "speechrecognition") {
       console.log("speechrecognition url")
       url = 'http://' + document.domain + ':' + port + '/tree?'
    }
    else if (projectname == "composer") {
       console.log("composer url")
       url = 'http://' + document.domain + ':' + port + '/tree?'
    }
    else if (projectname == "stockprediction") {
       console.log("stockprediction url")
       url = 'http://' + document.domain + ':' + port + '/tree?'
    }

    url = 'https://google.com';
    console.log(url)
    var link= document.getElementById('vnc_frame_src'); //or grab it by tagname etc
    link.href = url
    if (projectname == "pacman"){
         window.open(url, 'myiframe');}
    if (projectname == "antivirus"){
         window.open(url, 'myiframe');}
    if (projectname == "speechrecognition"){
         window.open(url, 'myiframe');}
    if (projectname == "composer"){
         window.open(url, 'myiframe');}
    if (projectname == "stockprediction"){
         window.open(url, 'myiframe');}

    var ssh_port_cookie = document.cookie.match(new RegExp('ssh_port=([^;]+)'));
    var ssh_port = !!ssh_port_cookie ? ssh_port_cookie[1] : null;
    console.log(ssh_port)

    if (projectname  == "R"){
          var command= document.getElementById('ssh_command');
          command.innerHTML = "ssh -p " + ssh_port + " root@" + document.domain
    }
    else{
          var command= document.getElementById('ssh_command');
          command.innerHTML = ""
    }
    //document.getElementById('vnc_frame').src = url
}

function loadFrameAfterDelete() {
    var command= document.getElementById('ssh_command');
    command.innerHTML = "Container Deleted."
    var link= document.getElementById('vnc_frame_src'); //or grab it by tagname etc
    link.href = 'http://' + document.domain + ':' + location.port + '/nocontainer'

}

function playVideo() {
    var video_name = $("input[name=projectname]:checked").val();
    var video_folder = '/video/';
    var video_path = video_folder.concat(video_name);
    console.log(video_path);

    var videoplayer = document.getElementById('videoplayer');

    videoplayer.src = video_path;
    videoplayer.play();
}

function dumpLogs() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/getlogs');
    var user_name_cookie = document.cookie.match(new RegExp('userID=([^;]+)'));
    var user_name = !!user_name_cookie ? user_name_cookie[1] : null;
    socket.on(user_name, function(line_received) {
        line_print = '<p>' + line_received + '<p>';
        $('#log').append(line_print);alert(line_print);
        document.getElementById("log").scrollTop = document.getElementById("log").scrollHeight;
    });
}
