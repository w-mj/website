
let server_url = null;
function sendMessage() {
    if (server_url === null)
        server_url = $('#server_url').html();
    let box = $("#input-box");
    let text = box.val();
    box.val('');
    console.log("say: " + text + " to: " + server_url);
    $("#chat-box").append("<li class=\"list-group-item message1\">" + text + "</li>");
    $.ajax({
        url: server_url,
        type: 'GET',
        data: {tk:'1', text:text},
        dataType: 'json',
        success: function (response) {
            $("#chat-box").append("<li class=\"list-group-item message2\">" + response.text + "</li>")
        },
        error: function (err) {
            console.log("chat server error");
            console.log(err);
        }
    });
}

function separation() {

}