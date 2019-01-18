$(document).ready(function () {
    $("#user-btn-group").hover(function () {
        $("#user-btn-group").prepend("<button type=\"button\" class=\"btn btn-outline-danger\" style=\"display: none;\">退出登陆</button>\n");
    }, function () {
        $("#user-btn-group").html("<button type=\"button\" class=\"btn btn-outline-success\" id=\"user-btn\">Middle</button>\n")
    })
});