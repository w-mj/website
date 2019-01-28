
function emo2emoji(emo) {
    if (emo >= 0 && emo < 0.25)
        return "😞";
    if (emo < 0.5)
        return "😑";
    if (emo < 0.75)
        return "😄";
    if (emo <= 1)
        return "😂";
    return "";
}

function html_encode(str)
{
  var s = "";
  if (str.length === 0) return "";
  s = str.replace(/&/g, "&gt;");
  s = s.replace(/</g, "&lt;");
  s = s.replace(/>/g, "&gt;");
  s = s.replace(/ /g, "&nbsp;");
  s = s.replace(/'/g, "&#39;");
  s = s.replace(/"/g, "&quot;");
  s = s.replace(/\n/g, "<br>");
  return s;
}

function sendMessage() {
    let box = $("#input-box");
    let text = box.val();
    if (text === "")
        return;
    let raw_text = text;
    text = html_encode(text);
    let chat_box = $("#chat-box");
    box.val('');
    console.log("say: " + text);
    chat_box.append(
        '<div class="chat-item" id="temp-message1">\n' +
            $("#say-template").html() +
            '<div class="message1">' + text + '</div>' +
        '<div class="emoji">' +
        '</div>'+
        '</div>'
    );
    chat_box.scrollTop(chat_box[0].scrollHeight);
    $.ajax({
        url: 'chat',
        type: 'POST',
        data: {text:raw_text, csrfmiddlewaretoken: Cookies.get('csrftoken')},
        dataType: 'json',
        success: function (response) {
            $("#temp-message1").remove();
            chat_box.append(
                '<div class="chat-item">\n' +
                    $("#say-template").html() +
                    '<div class="message1">' + text + '</div>' +
                '<div class="emoji">' + emo2emoji(response.emo) +
                '</div>'+
                '</div>'
            );
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

function synonym() {
    let w1 = $("#synonym-box-1").val();
    let w2 = $("#synonym-box-2").val();
    if (w1 === '' || w2 === '')
        return;
    $.ajax({
        url: 'synonym',
        type: 'GET',
        data: {w1: w1, w2: w2},
        success: function (response) {
            console.log(response);
            $("#synonym-result").html(response);
        },
        error: function (err) {
            console.log("synonym server error");
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


