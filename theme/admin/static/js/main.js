/**
 * Created by Nightsuki on 2016/4/6.
 */

$("#login-submit").click(function () {
    var username = $("#username").val();
    var password = $("#password").val();
    $.ajax({
        url: "/ajax/login",
        contentType: "application/json",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({username: username, password: password}),
        success: function (r) {
            if (r.status === "success") {
                window.location = "/admin";
            }
            else if (r.status === 'fail') {
                alert(r.result);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    })
});
