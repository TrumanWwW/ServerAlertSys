/*
* 初始化
* */
;$(function () {
    usersAuto();
    tableInit();
});

/**
 *   一些优化
 * */
function usersAuto() {
    $('#btn_add').on('click', function () {
        $('#myModal1').find('input:text,input:password').val('')
    });
}

/**
 *   bootstrap table初始化
 * */
function tableInit() {
    $('#table').bootstrapTable({
        url: '/api_v1/users/table',  // 请求数据源的路由
        dataType: "json",
        pagination: true, //前端处理分页
        singleSelect: false,//是否只能单选
        search: false, //显示搜索框，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        toolbar: '#toolbar', //工具按钮用哪个容器
        striped: true, //是否显示行间隔色
        cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pageNumber: 1, //初始化加载第10页，默认第一页
        pageSize: 10, //每页的记录行数（*）
        pageList: [10, 20, 50, 100], //可供选择的每页的行数（*）
        strictSearch: true,//设置为 true启用 全匹配搜索，false为模糊搜索
        showColumns: true, //显示内容列下拉框
        showRefresh: true, //显示刷新按钮
        minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
        clickToSelect: false, //设置true， 将在点击某行时，自动勾选rediobox 和 checkbox
        // {#        height: 500, //表格高度，如果没有设置height属性，表格自动根据记录条数决定表格高度#}
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        showToggle: true, //是否显示详细视图和列表视图的切换按钮
        cardView: false, //是否显示详细视图
        // {#        detailView: true, //是否显示父子表，设置为 true 可以显示详细页面模式,在每行最前边显示+号#}
        sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
        queryParams: function (params) {
            //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            var temp = {
                rows: params.limit,                         //页面大小
                page: (params.offset / params.limit) + 1,   //页码
                sort: params.sort,      //排序列名
                sortOrder: params.order //排位命令（desc，asc）
            };
            return temp;
        },
        columns: [{
            checkbox: true
        }, {  //定义表头,这个表头必须定义,下边field后边跟的字段名字必须与后端传递的字段名字相同.如:id、name、price
            field: 'seq',
            title: '序号',
            align: 'center',  //对齐方式，居中
            // {# width: '200px'  // 可以写各种样式#}
            formatter: function (value, row, index) {
                var e = index + 1;
                return e + ".";
            }  //对齐方式，居中
            // {# width: '200px'  // 可以写各种样式#}

        }, {
            field: 'id',
            title: '用户id',
            align: 'center'
        }, {
            field: 'name',
            title: '名称',
            align: 'center'
        }, {
            field: 'auth',
            title: '权限',
            align: 'center'
        }, {
            field: 'create_time',
            title: '创建时间',
            align: 'center'
        }, {
            title: '操作',
            field: 'id',
            align: 'center',
            formatter: function (value, row, index) {
                var e = '<a class="btn btn-xs blue"  data-toggle="modal" data-target="#myModal2" onclick="edit(this,\'' + row.id + '\')"><u>编辑</u><span class=\'glyphicon glyphicon-pencil\'></span></a>|';
                var f = '<a class="btn btn-xs blue"  data-toggle="modal" data-target="#myModal3" onclick="reset(this,\'' + row.id + '\')"><u>重设密码</u><span class=\'glyphicon glyphicon-repeat\'></span></a>|';
                var d = '<a class="btn btn-xs blue"  onclick="del(this,\'' + row.id + '\')" data-toggle="modal" data-target="#common_confirm_model"><u>删除</u><span class=\'glyphicon glyphicon-remove\'></span></a> ';
                return e + f + d;
            }
        }]
    });
}

/**
 * table操作edit()、reset()、del()
 * */
function edit(e, id) {
    // console.log(e);
    var $p = $(e).parents('tr');
    // var id = $p.find('td').eq(2).html();
    var name = $p.find('td').eq(3).html();
    var auth_str = $p.find('td').eq(4).html();
    var dict = {'ROOT': 2, '管理员': 1, '用户': 0};
    var $o = $('#myModal2');
    $o.find('.u_id').val(id);
    $o.find(':text').val(name);
    $o.find('option').eq(dict[auth_str]).attr('selected', 'selected')
}

function reset(e, id) {
    console.log(e)
}

function del(e, id) {
    // var b = confirm('确认要删除么？'), data_list = [];
    var b, data_list = [];
    Common.confirm({
        title: "注意",
        message: "确认要删除么？",
        operate: function (reselt) {
            reselt ? b=true:b=false;
            if (!b) {
                return false;
            }
            if (e) {
                //  单选
                var $p = $(e).parents('tr');
                data_list.push(id);
            } else {
                //  多选
                $('tbody :checkbox:checked').parents('tr').each(function () {
                    data_list.push($(this).attr('data-uniqueid'));
                });
            }
            var ajax1 = $.ajax({
                'url': '/users',
                'type': 'DELETE',
                'data': JSON.stringify({'data': data_list}),
                'contentType': 'application/json'
            }).done(function (data) {
                for (var k in data) {
                    toastr[k](data[k]);
                    $('#table').bootstrapTable('refresh');
                }

            })

        }
    });
}