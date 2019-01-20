changepsw_obj = null;


function changePsw() {
    let old_psw = $("#old-psw").val();
    let psw1 = $("#new-psw1").val();
    let psw2 = $("#new-psw2").val();
    if (old_psw === "") {
        $("#fail").html("必须填写旧密码").show();
        changepsw_obj.reset();
        return
    }
    if (psw1 === "") {
        $("#fail").html("必须填写新密码").show();
        changepsw_obj.reset();
        return
    }
    if (psw1 !== psw2) {
        $("#fail").html("两次输入密码不一致").show();
        changepsw_obj.reset();
        return;
    }
    $.ajax({
        url: "changepsw",
        method: "POST",
        data: $("#changepsw-form").serializeArray(),
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#fail").hide();
                $("#success").show();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                $("#fail").html(response.msg).show();
                changepsw_obj.reset();
            }
        },
        error: function (err) {
            let t = $("#fail");
            t.html("内部错误");
            t.show();
        }
    })
}

$(document).ready(function () {
    $("#upload-avatar").fileinput({
        language: 'zh',
        theme: 'fas',
        allowedFileExtensions: ['jpg', 'png', 'gif'],
        showClose: false,
        maxFileCount: 1,
        autoReplace: true,
        maxFileSize: 1024,
        uploadUrl: 'uploadavatar',
        uploadExtraData: {csrfmiddlewaretoken: Cookies.get('csrftoken')}
    }).on('fileuploaded', function(event, data, previewId, index) {
        window.location.reload();
    });

    initCaptcha(function (captchaObj) {
        captchaObj.appendTo("#changepsw-captcha");
        captchaObj.bindForm("#changepsw-form");
        window.changepsw_obj = captchaObj;
    });
});


function delete_history() {
    $.ajax({
        url: 'deletehistory',
        method: 'POST',
        data: {csrfmiddlewaretoken: Cookies.get('csrftoken')},
        success: function () {
            $("#delete-success").show();
        }
    })
}