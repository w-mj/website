function uperr(msg) {
    let box = $("#signin-fail");
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
            name: name,
            password: psw1
        },
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                let box = $("#signin-success");
                box.html("注册成功");
                box.show();
                Cookies.set('uid', 1);
                setTimeout(function () {
                    window.location.href='/';
                }, 3000);
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


