$(document).ready(function(){
    $.ajax({
     type: "GET",
     url: '/getFile',
     
     success: function(data) {
        document.getElementById("file").value = data;
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
            success: function(data) {
            document.getElementById("output").value = data;
        }
        });
    });
})