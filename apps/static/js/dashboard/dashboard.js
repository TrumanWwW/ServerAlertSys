/*
* 初始化
* */
;$(function () {
    horScroll();
    refreshServerList();//刷新服务器列表
    list_click();//绑定列表点击事件
    initCharts();//初始化图表
});

//图表参数
var myCharts = [];  //多个图表
var option_list = [];  // 多个图表的设置
var cpu_data = [];
var mem_data = [];
var disk_data = [];
// var load_data = [];
var timer;  //定时器
var s_id;
var active_index;

//更新图表数据
timer = setInterval(get_latest_data, 2000);

//更新列表数据
setInterval(refreshServerList, 10 * 1000);

//获取最新一组数据
function get_latest_data() {
    $.get({
        url: '/api_v1/dashboard/server/' + s_id
    }).done(function (data) {
        var time = data.timeStamp;
        cpu_data.push({
            name: time,
            value: [
                time,
                data.cpu_rate
            ]
        });
        mem_data.push({
            name: time,
            value: [
                time,
                data.mem_used_rate
            ]
        });
        disk_data.push({
            name: time,
            value: [
                time,
                data.disk_used_rate
            ]
        });
        // load_data.push({
        //     name: time,
        //     value: [
        //         time,
        //         data.loadIn1Min
        //     ]
        // });
    }).done(function (data) {
        option_list[0].series[0].data[0].value = cpu_data[cpu_data.length - 1].value[1];
        option_list[0].series[1].data[0].value = mem_data[mem_data.length - 1].value[1];
        option_list[0].series[2].data[0].value = disk_data[disk_data.length - 1].value[1];
        // option_list[0].series[3].data[0].value = load_data[load_data.length - 1].value[1];
        myCharts[0].setOption(option_list[0], true);


        //折线图
        if (cpu_data.length > 31) {
            cpu_data.shift();
            mem_data.shift();
            disk_data.shift();
            // load_data.shift();
        }
        option_list[1].xAxis[0].min = new Date() - 60 * 1000; //更新最小x坐标
        myCharts[1].setOption(option_list[1]);
        if(s_id){
           myCharts[0].hideLoading();
           myCharts[1].hideLoading();
        }else {
            toastr['warning'](data.warning)
        }

    })
}

//  绑定点击事件
function list_click() {
    $('#wrapper').on('click', '.urge,.free', function () {
        s_id = $(this).attr('s_id');
        active_index = $(this).index();
        $(this).addClass('active').siblings().removeClass('active');
        cpu_data.length = 0;
        mem_data.length = 0;
        disk_data.length = 0;
        // load_data.length = 0;
        clearInterval(timer);
        get_latest_data();
        timer = setInterval(get_latest_data, 2000);
    })
}

// 水平滚动
function horScroll() {
    var horwheel = require('horwheel');
    var view = document.getElementById('wrapper');
    horwheel(view);
}

//图表初始化
function initCharts() {
    var dom = document.getElementById("gauge");
    var dom2 = document.getElementById("lineStack");

    myCharts[0] = echarts.init(dom);
    myCharts[1] = echarts.init(dom2);

//折线图设置
//仪表图默认设置
    var default_inside_options = {
        name: 'CPU使用率',
        type: 'gauge',
        center: ['20%', '50%'],
        axisLine: {
            show: true,
            lineStyle: { // 属性lineStyle控制线条样式
                color: [ //表盘颜色
                    [0.25, "#28c656"],//90%-100%处的颜色
                    [0.5, "#f5e33e"],//70%-90%处的颜色
                    [0.75, "#ff9618"],//51%-70%处的颜色
                    [1, "#DA462C"]//0-50%处的颜色
                ],
                width: 7//表盘宽度
            }
        },
        axisLabel: { // 刻度标签
            distance: 1,
            textStyle: { // 属性lineStyle控制线条样式
                fontWeight: 'normal',
                fontStyle: 'oblique',
                color: 'auto',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            }
        },
        axisTick: { // 刻度样式
            length: 15, // 属性length控制线长
            lineStyle: { // 属性lineStyle控制线条样式
                color: 'auto',
                shadowColor: '#fff', //默认透明
                shadowBlur: 5
            }
        },
        splitLine: { // 分隔线
            length: 20, // 属性length控制线长
            lineStyle: { // 属性lineStyle（详见lineStyle）控制线条样式
                width: 1,
                color: 'auto',
                shadowColor: '#fff', //默认透明
                shadowBlur: 0
            }
        },
        pointer: { // 分隔线
            shadowColor: '#fff', //默认透明
            shadowBlur: 5,
            width: 3
        },
        title: {
            textStyle: { // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                fontWeight: 'bolder',
                fontSize: 20,
                fontStyle: 'italic',
                color: '#999',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            }
        },
        //指针下方数字显示#}
        detail: {
            backgroundColor: 'auto',
            borderWidth: 1,
            borderColor: '#999',
            shadowColor: '#fff', //默认透明
            shadowBlur: 0,
            offsetCenter: [0, '80%'], // x, y，单位px
            textStyle: { // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                fontWeight: 'bolder',
                color: '#fff',
                textBorderColor: '#000',
                textBorderWidth: 2,
                textShadowBlur: 2
            },
            formatter: function (value) {
                if(isNaN(value)){
                    return '--.--'
                }
                value = (value + '').split('.');
                value.length < 2 && (value.push('00'));
                return ('00' + value[0]).slice(-2)
                    + '.' + (value[1] + '00').slice(0, 2);
            }
        },
        data: [{
            value: 40,
            name: 'CPU%'
        }]

    };
    var inside_option2 = {}, inside_option3 = {}, inside_option4 = {};  //更新的设置
    option_list[0] = {
        title: {
            text: '实时状态'
        },
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },
        series: [
            default_inside_options,
            $.extend(inside_option2, default_inside_options, {
                name: '内存使用率',
                center: ['50%', '50%'],
                data: [{
                    name: 'MEM%'
                }]
            }),
            $.extend(inside_option3, default_inside_options, {
                name: '磁盘使用率',
                center: ['80%', '50%'],
                data: [{
                    name: 'DISK%'
                }]
            })
            // $.extend(inside_option4, default_inside_options, {
            //     name: '负载',
            //     center: ['87%', '50%'],
            //     data: [{
            //         name: 'LOAD%'
            //     }]
            // })
        ], animationDurationUpdate: 1000
    };
//折线图设置#}
    option_list[1] = {
        title: {
            text: '状态波动'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#283b56'
                }
            }
        },
        legend: {
            data: ['CPU%', 'MEM%', 'DISK%'] // no load
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'time',
                splitLine: {
                    show: false
                },
                splitNumber: 30,
                boundaryGap: false
            }
        ],
        yAxis: {
            type: 'value',
            min: 0,
            max: 100,
            boundaryGap: [0, '100%'],
            splitLine: {
                show: false
            }
        },
        series: [
            {
                name: 'CPU%',
                type: 'line',
                stack: 'CPU',
                data: cpu_data
            },
            {
                name: 'MEM%',
                type: 'line',
                stack: 'MEM',
                data: mem_data
            },
            {
                name: 'DISK%',
                type: 'line',
                stack: 'DISK',
                data: disk_data
            }
            // {
            //     name: 'LOAD%',
            //     type: 'line',
            //     stack: 'LOAD',
            //     data: load_data
            // }
        ], animationDurationUpdate: 700
    };
    myCharts[0].showLoading('default', {
        text: 'Loading...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'rgba(255, 255, 255, 0.8)'
    });
    myCharts[1].showLoading('default', {
        text: 'Loading...',
        color: '#c23531',
        textColor: '#000',
        maskColor: 'rgba(255, 255, 255, 0.8)'
    });


    function randomData() {
        value = Math.random() * 100;
        return {
            name: new Date().toString(),
            value: [
                new Date(),
                Math.round(value)
            ]
        }

    }

//窗口适应
    window.onresize = function () {
        myCharts[0].resize();
        myCharts[1].resize();
    };
}

//更新列表
function refreshServerList() {
    var $dom = $('<div>\n' +
        '<svg viewBox="0 0 1031 1024" version="1.1"\n' +
        'xmlns="http://www.w3.org/2000/svg">\n' +
        '<path d="M1024 198.4c-6.4-64-115.2-108.8-128-115.2l-179.2-76.8c-6.4 0-19.2 0-25.6 6.4s0 19.2 6.4 25.6c32 32 44.8 89.6 44.8 89.6 0 6.4 0 742.4 0 761.6 0 51.2-38.4 83.2-38.4 89.6-6.4 6.4-6.4 19.2-6.4 25.6 6.4 6.4 12.8 12.8 19.2 12.8 0 0 6.4 0 6.4 0 6.4 0 160-64 172.8-64 128-44.8 134.4-121.6 134.4-128l0-627.2zM531.2 0l-403.2 0c-70.4 0-128 57.6-128 134.4l0 755.2c0 76.8 57.6 134.4 128 134.4l396.8 0c70.4 0 128-57.6 128-134.4l0-755.2c6.4-76.8-51.2-134.4-121.6-134.4l0 0zM307.2 857.6c-44.8 0-76.8-38.4-76.8-83.2s38.4-83.2 76.8-83.2c44.8 0 76.8 38.4 76.8 83.2 6.4 44.8-32 83.2-76.8 83.2l0 0zM556.8 512c0 32-25.6 64-57.6 64l-339.2 0c-32-6.4-57.6-32-57.6-64l0-134.4 454.4 0 0 134.4zM556.8 307.2l-454.4 0 0-128c0-32 25.6-64 57.6-64l345.6 0c32 0 57.6 25.6 57.6 64l0 128z"></path>\n' +
        '</svg>\n' +
        '<p align="center"></p>\n' +
        '</div>');
    $.get({
        url: '/api_v1/dashboard/list'
    }).done(function (data) {
        $('#wrapper').empty();
        // s_id = s_id ? s_id : data[index].s_id;

        for (var index in data) {
            if (!s_id && data[index].state) {
                s_id = data[index].s_id;
                active_index = index
            }
            var className = 'col-md-1 col-sm-2';
            index == active_index ? className += ' active' : false;
            var $o = $dom.clone();
            switch (data[index].state) {
                case 'highLoad':
                    className += ' urge';
                    break;
                case true:
                    className += ' free';
                    break;
            }
            $o.attr({
                'title': data[index].name + '#' + data[index].ip,
                's_id': data[index].s_id,
                'class': className + ' pull-left'
            }).addClass(className);
            $o.find('p').html(data[index].name);
            $('#wrapper').append($o);
        }
    })
}