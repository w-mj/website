
function sendMessage() {
    let box = $("#input-box");
    let text = box.val();
    box.val('');
    console.log("say: " + text);
    $("#chat-box").append("<li class=\"list-group-item message1\">" + text + "</li>");
    $.ajax({
        url: 'chat',
        type: 'POST',
        data: {text:text, csrfmiddlewaretoken: Cookies.get('csrftoken')},
        dataType: 'json',
        success: function (response) {
            $("#chat-box").append("<li class=\"list-group-item message2\">" + response.text + "</li>");
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

$(document).ready(function () {
    console.log("ready");
    let btn = $("#logout-btn");
    btn.click(function () {
        $.ajax({
            url: 'logout',
            method: 'POST',
            data: {csrfmiddlewaretoken: Cookies.get('csrftoken')},
            success: function () {
                console.log("log out");
                Cookies.remove('uid');
                window.location.href='/';
            }
        });
    });
    let name = "";
    btn.hover(function () {
        name = btn.html();
        btn.html("退出登陆");
    }, function () {
        btn.html(name);
    })
});