function initCaptcha(callback) {
    $.ajax({
        url: "pc-geetest/get?t=" + (new Date()).getTime(),
        type: "get",
        dataType: "json",
        width: '100%',
        success: function (data) {
            //请检测data的数据结构， 保证data.gt, data.challenge, data.success有值
            initGeetest({
                // 以下配置参数来自服务端 SDK
                gt: data.gt,
                challenge: data.challenge,
                offline: !data.success,
                new_captcha: true
            }, callback)
        }
    });
}
