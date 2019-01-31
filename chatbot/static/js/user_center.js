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

function classifyDate(date) {
    let result = {};
    for (let i = 0; i < date.length; i++) {
        let line = date[i];
        let sp = line[0].split(' ');

        if (!(sp[0] in result))
            result[sp[0]] = [];
        result[sp[0]].push(line);
    }
    return result;
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

    $.ajax({
        url: 'statistics',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            echarts.init(document.getElementById('emotion-chart')).setOption({
                series: [{
                    type: 'pie',
                    data: [
                        {value: response.A, name: '😞'},
                        {value: response.B, name: '😑'},
                        {value: response.C, name: '😄'},
                        {value: response.D, name: '😂'},
                    ],
                    label: {
                        formatter: '{b}: {c}'
                    }
                }]
            });
            let line_chart_data = classifyDate(response.detail);
            let line_space = $("#emotion-line");
            line_space.html('');
            for (let date in line_chart_data) {
                let time = line_chart_data[date];
                line_space.append('<div id="line-chart-' + date + '" style="width: 600px;height:200px;"> </div>');
                echarts.init(document.getElementById('line-chart-' + date)).setOption({
                    title: {
                        text: date
                    },
                    xAxis: {
                        type: 'time',
                        minInterval: 1,
                        axisLabel: {
                            formatter: function(value, index) {
                                return new Date(value).format("H:i:s")
                            }
                        }
                    },
                    yAxis: {
                        type: 'value',
                        min: 0,
                        max: 1,
                    },
                    series: [{
                        type: 'line',
                        smooth: true,
                        data: time
                    }]
                });
            }
        }
    })
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