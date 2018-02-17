$(document).ready(function(){
    $.ajax({
            type: "POST",
            url: "/get_env_list",
            success: function(response) {
                create_checklist(response);
            }
    });

    $("#remove").click(function() {
        var envs = get_checked_envs()
        $.ajax({
            type: 'POST',
            url: '/remove_envs',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({data:envs}),
        });
    });
})


function create_checklist(names){
    var arrayLength = names.length;
    for (var i = 0; i < arrayLength; i++) {
        add_checkbox(names[i]);
    }
}

function add_checkbox(name) {
    var br = document.createElement('br');
    var label= document.createElement("label");
    var description = document.createTextNode(name);
    var checkbox = document.createElement("input");

    checkbox.type = "checkbox";    // make the element a checkbox
    checkbox.name = name;      // give it a name we can check on the server side
    checkbox.value = name;         // make its value "pair"

    label.appendChild(checkbox);   // add the box to the element
    label.appendChild(description);// add the description to the element

    // add the label element to your div
    document.getElementById('envs').appendChild(label);
    document.getElementById('envs').appendChild(br);
}

function get_checked_envs(){
    var selected = [];
    $('#envs input:checked').each(function() {
        selected.push($(this).attr('name'));
    });
    return selected
}
