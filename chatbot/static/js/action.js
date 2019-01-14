
function sendMessage() {
    let box = $("#input-box");
    let text = box.val();
    box.val('');
    console.log("say: " + text);
    $("#chat-box").append("<li class=\"list-group-item message1\">" + text + "</li>");
    $.ajax({
        url: 'chat',
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
    let box = $("#to-separation");
    t = box.val();
    $.ajax({
        url: 'separation',
        type: 'GET',
        data: {"text": t},
        success: function (response) {
            console.log(response);
            box.val(response);
        },
        error: function (err) {
            console.log("separation server error");
            console.log(err);
        }
    });
}