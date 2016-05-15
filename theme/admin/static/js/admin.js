/**
 * Created by Nightsuki on 2016/5/11.
 */

$(document).ready(function () {
    $("#login").click(function (e) {
        e.preventDefault();
        var data = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        $.ajax({
            url: '/ajax/login',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    window.location.href = "/admin";
                }
                else if (r.status === 'fail') {
                    alert(r.result);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });
    $("#user_edit_submit").click(function (e) {
        e.preventDefault();
        var data = {
            action: "edit",
            user_id: $('#user_id').val(),
            nickname: $('#nickname').val(),
            password: $('#password').val(),
            mobilePhone: $('#mobilePhone').val(),
            role: $('#role').val()
        };
        $.ajax({
            url: '/admin/ajax/user',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                }
                else if (r.status === 'fail') {
                    alert(r.result);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });

    $("#user_delete_submit").click(function () {
        e.preventDefault();
        var user_list = $("input:checked");
        var user_id = [];
        user_list.each(function () {
            user_id.push($(this).val());
        });
        var data = {
            action: "delete",
            user_id: user_id
        };
        $.ajax({
            url: '/admin/ajax/user',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                }
                else if (r.status === 'fail') {
                    alert(r.result);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });

});