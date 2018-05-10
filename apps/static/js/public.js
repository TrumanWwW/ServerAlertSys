$(document).ready(function () {
    checkAuto();
    dropdownOpen();  //dropdown移上弹出子菜单
    nav_active();
    alert_ani();
    toastr_init();
});


/**
 *   一些优化
 * */
function checkAuto() {
    //关闭自动检查和填充
    $('input[type=text]').attr({
        'autocomplete': "off",
        'spellcheck': 'false'
    });
}

/**
 * dropdown移上弹出子菜单
 */
function dropdownOpen() {
    var $dropdownLi = $('.dropdown');

    $dropdownLi.mouseover(function () {
        $(this).addClass('open');
    }).mouseout(function () {
        $(this).removeClass('open');
    });
}

/**
 * 添加active判断
 * */
function nav_active() {
    $('.navbar-nav').find('a').each(function () {
        if (this.href == document.location.href || document.location.href.search(this.href) >= 0) {
            $(this).parent('li').addClass('active'); // this.className = 'active';
            $(this).parents('.dropdown-menu').prev().addClass('active');
        }
    });
}

/**
 *   alert框动画
 * */
function alert_ani() {
    $(".alert").delay(3000).slideUp(200, function () {
        $(this).alert('close');
    });
}

/**
 *   toastr
 * */
function toastr_init() {
    $('.toast-close-button.dis_show').click(function () {
        $('.toast-top-right.dis_pos').css('display', 'none')
    });
    if (sessionStorage.getItem("success")) {
        toastr.success(sessionStorage.getItem("success"));
        sessionStorage.clear();
    }
    if (sessionStorage.getItem("error")) {
        toastr.error(sessionStorage.getItem("error"));
        sessionStorage.clear();
    }
    if (sessionStorage.getItem("warning")) {
        toastr.warning(sessionStorage.getItem("warning"));
        sessionStorage.clear();
    }
    if (sessionStorage.getItem("info")) {
        toastr.info(sessionStorage.getItem("info"));
        sessionStorage.clear();
    }
    window.setTimeout(function () {
        $(".toast-top-right.dis_pos").children(':last').fadeTo(1000, 0).slideUp(1000, function () {
            $(this).remove();
        });
    }, 3000);
    toastr.options = {
        "closeButton": true,
        "timeOut": 3000,
        "debug": false,
        "onclick": null,
        "progressBar": false
    };
}

/*
*   confirm
* */
var Common = {
    confirm: function (params) {
        var model = $("#common_confirm_model");
        model.find(".title").html(params.title);
        model.find(".message").html(params.message);

        $("#common_confirm_btn").click();
        //每次都将监听先关闭，防止多次监听发生，确保只有一次监听
        model.find(".cancel").off("click");
        model.find(".ok").off("click");

        model.find(".ok").on("click", function () {
            params.operate(true)
            // return true
        });

        model.find(".cancel").on("click", function () {
            params.operate(false)
            // return false
        })
    }
};