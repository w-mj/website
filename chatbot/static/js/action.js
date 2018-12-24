

function sendMessage() {
    let box = $("#input-box");
    let text = box.val();
    box.val('');
    console.log("say: " + text);
    $("#chat-box").append("<li class=\"list-group-item message1\">" + text + "</li>");
    $.ajax({
        url: 'http://127.0.0.1:8000/chat',
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