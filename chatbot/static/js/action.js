
function sendMessage() {
    let box = $("#input-box");
    let text = box.val();
    let chat_box = $("#chat-box");
    box.val('');
    console.log("say: " + text);
    chat_box.append(
        '<div class="chat-item">\n' +
            $("#say-template").html() +
            '<div class="message1">' + text + '</div>' +
        '</div>'
    );
    chat_box.scrollTop(chat_box[0].scrollHeight);
    $.ajax({
        url: 'chat',
        type: 'POST',
        data: {text:text, csrfmiddlewaretoken: Cookies.get('csrftoken')},
        dataType: 'json',
        success: function (response) {
            chat_box.append(
                '<div class="chat-item">\n' +
                    $("#response-template").html() +
                    '<div class="message2">' + response.text + '</div>' +
                '</div>');
            chat_box.scrollTop(chat_box[0].scrollHeight);
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

function sentiment() {
    let box = $("#to-sentiment");
    t = box.val();
    $.ajax({
        url: 'sentiment',
        type: 'GET',
        data: {"text": t},
        success: function (response) {
            console.log(response);
            $("#sentiment-result").html(response);
        },
        error: function (err) {
            console.log("sentiment server error");
            console.log(err);
        }
    });
}

$(document).ready(function () {
    console.log("ready");
    let btn = $("#logout-btn");
    let name = "";
    btn.hover(function () {
        name = btn.html();
        btn.html("个人中心");
    }, function () {
        btn.html(name);
    });


    $("body").keydown(function() {
        if (event.keyCode === 13) { //keyCode=13是回车键
            sendMessage();
        }
    });
    let chat_box = $("#chat-box");
    chat_box.scrollTop(chat_box[0].scrollHeight);
});

