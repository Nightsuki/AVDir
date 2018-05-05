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
            username: $('#nickname').val(),
            nickname: $('#nickname').val(),
            password: $('#password').val(),
            email: $('#email').val(),
            role: $('#role').val()
        };
        $.ajax({
            url: '/ajax/user',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                    window.location.href = "/admin/user/list"
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

    $("#user_add_submit").click(function (e) {
        e.preventDefault();
        var data = {
            action: "add",
            user_id: $('#user_id').val(),
            username: $('#username').val(),
            nickname: $('#nickname').val(),
            password: $('#password').val(),
            email: $('#email').val(),
            role: $('#role').val()
        };
        $.ajax({
            url: '/ajax/user',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                    window.location.href = "/admin/user/list"
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


    $("#archive_add_submit").click(function (e) {
        e.preventDefault();
        var tag_list = $('#tags').tokenfield('getTokens');
        var tags = [];
        tag_list.forEach(function (one) {
            tags.push(one.value);
        });
        var data = {
            action: "add",
            archive_id: $('#archive_id').val(),
            title: $('#title').val(),
            slug: $('#slug').val(),
            type: $('#type').val(),
            status: $('#status').val(),
            content: $('#content').find('textarea').val(),
            tags: tags
        };
        $.ajax({
            url: '/ajax/archive',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                    window.location.href = "/admin/archive/list"
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

    $("#archive_edit_submit").click(function (e) {
        e.preventDefault();
        var tag_list = $('#tags').tokenfield('getTokens');
        var tags = [];
        tag_list.forEach(function (one) {
            tags.push(one.value);
        });
        var data = {
            action: "edit",
            archive_id: $('#archive_id').val(),
            title: $('#title').val(),
            slug: $('#slug').val(),
            type: $('#type').val(),
            status: $('#status').val(),
            content: $('#content').find('textarea').val(),
            tags: tags
        };
        $.ajax({
            url: '/ajax/archive',
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: 'JSON',
            success: function (r) {
                if (r.status === "success") {
                    alert(r.result);
                    window.location.href = "/admin/archive/list"
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

function user_del(user_id) {
    var data = {
        action: "del",
        user_id: user_id
    };
    $.ajax({
        url: '/ajax/user',
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: 'JSON',
        success: function (r) {
            if (r.status === "success") {
                alert(r.result);
                location.reload()
            }
            else if (r.status === 'fail') {
                alert(r.result);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    });
}

function archive_del(archive_id) {
    var data = {
        action: "del",
        archive_id: archive_id
    };
    $.ajax({
        url: '/ajax/archive',
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: 'JSON',
        success: function (r) {
            if (r.status === "success") {
                alert(r.result);
                window.location.href = "/admin/archive/list"
            }
            else if (r.status === 'fail') {
                alert(r.result);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    });
}