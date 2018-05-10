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

}

/*
*   表格初始化
* */
function tableInit() {
    $('#table').bootstrapTable({
        url: '/api_v1/log/operation/table',  // 请求数据源的路由
        dataType: "json",
        pagination: true, //前端处理分页
        singleSelect: false,//是否只能单选
        search: false, //显示搜索框，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        toolbar: '#toolbar', //工具按钮用哪个容器
        striped: true, //是否显示行间隔色
        cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        sortable: true, //是否启用排序
        sortName: 'id',//初始化的时候排序的字段
        sortOrder: "desc", //排序方式
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
                sortOrder: params.order, //排位命令（desc，asc）
                type: $('#toolbar :selected').val() || null
            };
            return temp;
        },
        columns: [{
            checkbox: false,
            visible: false
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
            field: 'id',
            title: '操作id',
            align: 'center',
            sortable: true
        }, {
            field: 'time',
            title: '时间',
            align: 'center'
        }, {
            field: 'module',
            title: '模块',
            align: 'center'
        }, {
            field: 'operation',
            title: '操作',
            align: 'center'
        }, {
            field: 'res',
            title: '结果',
            align: 'center'
        }, {
            field: 'u_name',
            title: '用户',
            align: 'center'
        }],
        onEditableSave: function (field, row, oldValue, $el) {
            update_row(field, row, oldValue, $el)
        }
    });
}

$('#toolbar').find('select').bind('change', function () {
    $('#table').bootstrapTable('refresh',{silent: true});
});
