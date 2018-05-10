/*
* 初始化
* */
;$(function () {
    before_init();
    tableInit();
});

/**
 *   一些优化
 * */
function before_init() {
    $('#btn_add').bind('click', function () {
        $('#myModal1 :text').val('');
    })
}

/**
 *   bootstrap table初始化
 * */
function tableInit() {
    $('#table').bootstrapTable({
        url: '/api_v1/alert/table',  // 请求数据源的路由
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
        showToggle: false, //是否显示详细视图和列表视图的切换按钮
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
        }, {
            //定义表头,这个表头必须定义,下边field后边跟的字段名字必须与后端传递的字段名字相同.如:id、name、price
            field: 'seq',
            title: '序号',
            align: 'center',  //对齐方式，居中
            // {# width: '200px'  // 可以写各种样式#}
            formatter: function (value, row, index) {
                var e = index + 1;
                return e + ".";
            }
        }, {
            field: 's_id',
            title: '服务器id',
            align: 'center'
        }, {
            field: 's_name',
            title: '名称',
            align: 'center'
        }, {
            field: 'ip',
            title: 'IP',
            align: 'center'
        }, {
            field: 's_cpu_th',
            title: 'CPU阈值(%)',
            align: 'center',
            editable: {
                type: 'text',
                title: 'CPU阈值(0~100)',
                validate: function (val) {
                    if (isNaN(val)) {
                        return '必须是数字'
                    }
                    if (val > 100 || val < 0) {
                        return '数字范围0~100'
                    }
                }
            }
        }, {
            field: 's_mem_th',
            title: '内存阈值(%)',
            align: 'center',
            editable: {
                type: 'text',
                title: '内存阈值(0~100)',
                validate: function (val) {
                    if (isNaN(val)) {
                        return '必须是数字'
                    }
                    if (val > 100 || val < 0) {
                        return '数字范围0~100'
                    }
                }
            }
        }, {
            field: 's_disk_th',
            title: '磁盘阈值(%)',
            align: 'center',
            editable: {
                type: 'text',
                title: '磁盘阈值(0~100)',
                validate: function (val) {
                    if (isNaN(val)) {
                        return '必须是数字'
                    }
                    if (val > 100 || val < 0) {
                        return '数字范围0~100'
                    }
                }
            }
        }, {
            field: 'state',
            title: '监控状态',
            align: 'center',
            formatter: function (val, row, index) {
                var cls, str;
                if (row.state) {
                    cls = 'btn-success';
                    str = '监控中'
                } else {
                    cls = 'btn-warning';
                    str = '未监控'
                }
                return '<button class="btn btn-xs ' + cls + '" onclick="change_state(this,' + row.s_id + ')">' + str + '</button>'
            }
        }, {
            field: 'id',
            title: '操作',
            align: 'center',
            formatter: function (value, row, index) {
                var d = '<a class="btn btn-xs blue" data-delete-id="' + row.s_id + '" onclick="del(this,' + row.s_id + ',' + row.id + ') " data-toggle="modal" data-target="#common_confirm_model"><u>删除</u><span class=\'glyphicon glyphicon-remove\'></span></a> ';
                return d;
            }
        }],
        onEditableSave: function (field, row, oldValue, $el) {
            update_row(field, row, oldValue, $el)
        }
    });
}

function update_row(field, row, oldValue, arg) {
    $.ajax({
        type: "put",
        url: "/api_v1/alert/table",
        data: JSON.stringify(row),
        dataType: 'JSON',
        contentType: "application/json",
        success: function (data, status) {
            for (var k in data) {
                toastr[k](data[k]);
                // $('#table').bootstrapTable('refresh');
            }
        },
        error: function () {
            toastr['error']('更改失败，请检查网络');
            $('#table').bootstrapTable('refresh');
        },
        complete: function (data) {
        }
    });
}

/**
 * table操作edit()、changeState()、del()
 * */
function edit(e, id) {
    // console.log(e);
    // var $tr = $(e).parents('tr');
    // var $o = $('#myModal2');
    // $tr.find('td').slice(2, 11).each(function (index) {
    //     $o.find(':text,[name=s_id]').eq(index).val($(this).html());
    // });
}

function change_state(e, s_id) {
    var uniqueid = $(e).parents('tr').attr('data-uniqueid');
    var b = $(e).hasClass('btn-success');
    $(e).parents('#table').bootstrapTable('getRowByUniqueId', uniqueid);
    if (b) {
        $(e).removeClass('btn-success').addClass('btn-warning').html('未监控')
    } else {
        $(e).removeClass('btn-warning').addClass('btn-success').html('监控中')
    }
    update_row(false, {'id': uniqueid, 'state': !b})
}

function del(e, s_id, id) {
    var b, data_list = [];
    Common.confirm({
        title: "注意",
        message: "<u>将删除对应服务器</u>，确认要删除么？",
        operate: function (reselt) {
            if (reselt) {
                b = true
            } else {
                b = false
            }
            if (!b) {
                return false;
            }
            if (e && s_id) {
                //  单选
                data_list.push(s_id);
            } else {
                //  多选
                $('tbody :checkbox:checked').parents('tr').each(function () {
                    data_list.push($(this).find('td:last a').attr('data-delete-id'));
                });
            }
            var ajax1 = $.ajax({
                'url': '/config/server',
                'type': 'DELETE',
                'data': JSON.stringify({'data': data_list}),
                'contentType': 'application/json'
            }).done(function (data) {
                for (var k in data) {
                    toastr[k](data[k]);
                    // $('#table').bootstrapTable('removeByUniqueId', id);
                    $('#table').bootstrapTable('refresh',{silent: true});
                }
            })
        }
    })
}