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
        return
    }
    if (psw1 === "") {
        uperr("必须填写密码");
        return
    }
    if (psw1 !== psw2) {
        uperr("两次输入密码不一致");
        return;
    }
    $.ajax({
        url: "signup",
        method: "POST",
        data: {
            csrfmiddlewaretoken: Cookies.get('csrftoken'),
            username: name,
            password: psw1
        },
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#signup-success").show();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                uperr(response.msg)
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
        return
    }
    if (psw1 === "") {
        inerr("必须填写密码");
        return
    }
        $.ajax({
        url: "signin",
        method: "POST",
        data: {
            csrfmiddlewaretoken: Cookies.get('csrftoken'),
            username: name,
            password: psw1
        },
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#signin-success").show();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                inerr(response.msg)
            }
        },
        error: function (err) {
            console.log(err);
            inerr("内部错误");
        }
    })
}

