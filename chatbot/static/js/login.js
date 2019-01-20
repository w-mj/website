signup_obj = null;
signin_obj = null;
$(document).ready(function () {
    initCaptcha(function (captchaObj) {
        captchaObj.appendTo("#signup-captcha");
        captchaObj.bindForm("#signup-form");
        window.signup_obj = captchaObj;
    });
    initCaptcha(function (captchaObj) {
        captchaObj.appendTo("#signin-captcha");
        captchaObj.bindForm("#signin-form");
        window.signin_obj = captchaObj;
    });
});



function uperr(msg) {
    let box = $("#signup-fail");
    box.html(msg);
    box.show();
}

function signup() {
    let name = $("#signup-name").val();
    let psw1 = $("#signup-psw1").val();
    let psw2 = $("#signup-psw2").val();
    if (name === "") {
        uperr("必须填写用户名");
        signup_obj.reset();
        return
    }
    if (psw1 === "") {
        uperr("必须填写密码");
        signup_obj.reset();
        return
    }
    if (psw1 !== psw2) {
        uperr("两次输入密码不一致");
        signup_obj.reset();
        return;
    }
    $.ajax({
        url: "signup",
        method: "POST",
        data: $("#signup-form").serializeArray(),
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#signup-success").show();
                $("#signup-fail").hide();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                uperr(response.msg);
                signup_obj.reset();
            }
        },
        error: function (err) {
            console.log(err);
            uperr("内部错误");
        }
    })
}


function inerr(msg) {
    let box = $("#signin-fail");
    box.html(msg);
    box.show();
}

function signin() {
    let name = $("#signin-name").val();
    let psw1 = $("#signin-psw1").val();
    if (name === "") {
        inerr("必须填写用户名");
        signin_obj.reset();
        return
    }
    if (psw1 === "") {
        inerr("必须填写密码");
        signin_obj.reset();
        return
    }
        $.ajax({
        url: "signin",
        method: "POST",
        data: $("#signin-form").serializeArray(),
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#signin-success").show();
                $("#signin-fail").hide();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                inerr(response.msg);
                signin_obj.reset();
            }
        },
        error: function (err) {
            console.log(err);
            inerr("内部错误");
        }
    })
}