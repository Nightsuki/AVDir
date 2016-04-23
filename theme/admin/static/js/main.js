/**
 * Created by Nightsuki on 2016/4/6.
 */
$(".create-note").click(function () {
    do_create_note()
});

$(".create-collection").click(function () {
    do_create_collection()
});

$("#profile-submit").click(function () {
    var nickname = $("#nickname").val();
    var password = $("#password").val();
    $.ajax({
        url: "/ajax/profile",
        contentType: "application/json",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({nickname: nickname, password: password}),
        success: function (r) {
            if (r.status === "success") {
                $(".alert-success").text("修改成功!");
                $(".alert-success").toggle();
                setTimeout("$('.alert-success').toggle()", 1000);
            }
            else if (r.status === 'fail') {
                $(".alert-danger").text(r.result);
                $(".alert-danger").toggle();
                setTimeout("$('.alert-danger').toggle()", 1000);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    })
});

$("#signup-submit").click(function () {
    signup()
});

$(".signup-password").keydown(function (e) {
    var key = e.which;
    if (key == 13) {
        e.preventDefault();
        signup()
    }
});

$(".login-password").keydown(function (e) {
    var key = e.which;
    if (key == 13) {
        e.preventDefault();
        login()
    }
});

$("#login-submit").click(function () {
    login()
});

$('.login').find('input, textarea').on('keyup blur focus', function (e) {

    var $this = $(this),
        label = $this.prev('label');

    if (e.type === 'keyup') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.removeClass('highlight');
        }
    } else if (e.type === 'focus') {

        if ($this.val() === '') {
            label.removeClass('highlight');
        }
        else if ($this.val() !== '') {
            label.addClass('highlight');
        }
    }
});

$('.login .tab a').on('click', function (e) {
    e.preventDefault();
    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');
    var target = $(this).attr('href');
    $('.tab-content > div').not(target).hide();
    $(target).fadeIn(600);

});

function do_create_note() {
    $.ajax({
        url: "/ajax/note",
        contentType: "application/json",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({action: "create", collection_hash: collection_hash}),
        success: function (r) {
            if (r.status === "success") {
                window.location.href = "/note/" + r.result;
            }
            else if (r.status === 'fail') {
                alert(r.result);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    })
}

function do_create_collection() {
    var title = $('#collection-title').val();
    if (title) {
        $.ajax({
            url: "/ajax/collection",
            contentType: "application/json",
            type: "POST",
            dataType: "JSON",
            data: JSON.stringify({action: "create", title: title}),
            success: function (r) {
                if (r.status === "success") {
                    window.location.href = "/note/" + r.result;
                }
                else if (r.status === 'fail') {
                    alert(r.result);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        })
    } else {
        alert("请输入标题");
    }
}

function login() {
    $.ajax({
        url: "/ajax/login",
        contentType: "application/json",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({
            username: $("#login").find(".username").val(),
            password: $("#login").find(".login-password").val()
        }),
        success: function (r) {
            if (r.status === "success") {
                $(".alert-success").text("登录成功, 正在跳转...");
                $(".alert-success").toggle();
                setTimeout("window.location.href = '/note'", 1000);
            }
            else if (r.status === 'fail') {
                $(".alert-danger").text(r.result);
                $(".alert-danger").toggle();
                setTimeout("$('.alert-danger').toggle();", 1000);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    })
}

function signup() {
    $.ajax({
        url: "/ajax/signup",
        contentType: "application/json",
        type: "POST",
        dataType: "JSON",
        data: JSON.stringify({
            username: $("#signup").find(".username").val(),
            password: $("#signup").find(".signup-password").val()
        }),
        success: function (r) {
            if (r.status === "success") {
                $(".alert-success").text("注册成功, 正在跳转...");
                $(".alert-success").toggle();
                setTimeout("window.location.href = '/note'", 1000);
            }
            else if (r.status === 'fail') {
                $(".alert-danger").text(r.result);
                $(".alert-danger").toggle();
                setTimeout("$('.alert-danger').toggle();", 1000);
            }
        },
        error: function (r) {
            alert(r.info);
        }
    })
}

function reload_url(url) {
    if (history.pushState) {
        var state = ({
            url: url,
            title: ""
        });
        window.history.pushState(state, "", url);
    }
}