// Define selectedValue as a global variable
var selectedValue;

function populateSelectList() {
    fetch('/static/jsons/options.json')
        .then(response => response.json())
        .then(data => {
            const selectList = document.getElementById('selectList');
            selectList.innerHTML = '';
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.value;
                option.text = item.text;
                selectList.appendChild(option);
            });
            // Assign a value to selectedValue after the select list options are generated
            selectedValue = selectList.options[selectList.selectedIndex].value;
            selectList.dispatchEvent(new Event('change'));
        })
        .catch(error => console.error('Error:', error));
}

populateSelectList();
// 左上性别比例
function echarts_1(apiURL) {
    // 基于准备好的dom，初始化echarts实例
    var myChart1 = echarts.init(document.getElementById('echart1'));

    option1 = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        series: [{
            name: '占比情况',
            type: 'pie',
            radius: '80%',
            center: ['50%', '50%'],
            clockwise: false,
            data: [],
            label: {
                normal: {
                    textStyle: {
                        color: 'rgb(67,67,67)',
                        fontSize: 18,
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            itemStyle: {
                normal: {
                    //borderWidth: 1,
                    //borderColor: '#ffffff',
                },
                emphasis: {
                    borderWidth: 0,
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }],
        color: ['#9c88e7', '#54b2ff'],
        //backgroundColor: '#fff'
    };

    //让我们后端django 允许跨域
    axios.get(apiURL)
        .then(function (response) {
            // 当请求成功的时候，response就是后台发送过来数据
            console.log(response.data); //在控制台中查看数据是否正常返回
            option1.series[0].data = [];
            response.data.forEach(function (elem, index, arr) {
                console.log(elem, index);
                // option1.series[0].data.push({ 'name': elem.gender, 'value': elem.gender_count})
                if (elem.gender === 'f') {
                    option1.series[0].data.push({ 'name': '女', 'value': elem.gender_count })
                } else {
                    option1.series[0].data.push({ 'name': '男', 'value': elem.gender_count })
                }
            });
            myChart1.setOption(option1)

            //{name:'',value:''}
            //=
        })
        .catch(function (error) {
            // 当请求失败的时候，我们如何来处理
            console.log(error);
        })
        .finally(function () {
            // always executed
        });


    // 使用刚指定的配置项和数据显示图表。
    // myChart1.setOption(option1);
    window.addEventListener("resize", function () {
        myChart1.resize();
    });
}
// 每天博文统计
function echarts_2(apiURL) {
    // 基于准备好的dom，初始化echarts实例
    var myChart2 = echarts.init(document.getElementById('echart2'));

    option2 = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },

        "color": [ "#2f89cf"],

        grid: {
            top: '14%',
            left: '15',
            right: '35',
            bottom: '12%',
            containLabel: true
        },

        series: [
            {
                name: "分时段博文数统计（每天）",
                type: "bar",
                itemStyle: {
                    normal: { color: '' }
                },
                barWidth: '15',
                data: []
            }

        ],
        xAxis: {
            type: 'category',
            data: [],
            axisLabel: {
                show: true,
                textStyle: {
                    color: 'rgba(112,166,227,.6)'
                }
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(112,166,227,.5)'
                }
            },

            // data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        },

        yAxis: [{
            name: '',
            type: 'value',
            axisTick: { show: false },
            splitLine: {
                show: true,
                lineStyle: {
                    color: "#70a6e3"
                }
            }, //x轴线
            axisLabel: { show: true, textStyle: { color: 'rgba(112,166,227,.6)' } },
            axisLine: { lineStyle: { color: 'rgba(112,166,227,.5)' } },
        }],

    };

    axios.get(apiURL)
        .then(function (response) {
            // 当请求成功的时候，response就是后台发送过来数据
            console.log(response.data); //在控制台中查看数据是否正常返回
            timelist = []
            dataList = []
            response.data.forEach(function (elem, index, arr) {
                //console.log(elem, index);
                timelist.push(elem.post_time)
                dataList.push(parseInt(elem.post_amount))
            });
            console.log(timelist)
            console.log(dataList)
            option2.xAxis.data = timelist
            option2.series[0].data = dataList
            myChart2.setOption(option2);
        })
        .catch(function (error) {
            // 当请求失败的时候，我们如何来处理
            console.log(error);
        })
        .finally(function () {
            // always executed
        });

    // 使用刚指定的配置项和数据显示图表。
    // myChart2.setOption(option2);
    window.addEventListener("resize", function () {
        myChart2.resize();
    });
}
// 地图
function echarts_3(apiURL) {
    var myChart3 = echarts.init(document.getElementById('echart3'));


    var color = ['#fff'];
    var series = [];

    option3 = {
        //  backgroundColor: '#404a59',
        title: {
            text: '全国省份博文数统计',
            // subtext: '副标题，不需要主删除此行',
            left: 'center',
            top: '5%',
            textStyle: {
                color: '#638ab3'
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                console.log(params)
                if (params.name) {
                    return params.name + ' : ' + (isNaN(params.value) ? 0 : parseInt(params.value));
                }
            }
        },
        visualMap: {

            type: 'continuous', // continuous 类型为连续型  piecewise 类型为分段型
            show: false, // 是否显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
            // 指定 visualMapContinuous 组件的允许的最小/大值。'min'/'max' 必须用户指定。
            // [visualMap.min, visualMax.max] 形成了视觉映射的『定义域』

            // 文本样式
            textStyle: {
                fontSize: 17,
                color: '#fff'
            },
            realtime: false, // 拖拽时，是否实时更新
            calculable: true, // 是否显示拖拽用的手柄
            // 定义 在选中范围中 的视觉元素
            inRange: {
                color: ['#4098e0',
                    '#3d7ece',
                    '#1049a6'] // 图元的颜色
            },
        },

        series: [
            {
                name: '省份',
                type: 'map',
                mapType: 'china',
                roam: true,
                itemStyle: {
                    areaColor: '#4098e0', // 地图区域的颜色 如果设置了visualMap，areaColor属性将不起作用
                    borderWidth: 0.5, // 描边线宽 为 0 时无描边
                    borderColor: '#ffffff', // 图形的描边颜色 支持的颜色格式同 color，不支持回调函数
                    borderType: 'solid', // 描边类型，默认为实线，支持 'solid', 'dashed', 'dotted'
                    emphasis: {
                        show: true,
                        areaColor: '#54b2ff', // 鼠标划过的颜色
                        label: {
                            show: true,
                            textStyle: {
                                color: 'black'
                            }
                        }
                    }
                },
                label: {
                    normal: {
                        show: true,// 是否显示对应地名
                        textStyle: {
                            color: 'white'
                        }
                    },
                },
                data: [],
                zoom: 1.2,
            }
        ]
    };


    axios.get(apiURL)
        .then(function (response) {
            // 当请求成功的时候，response就是后台发送过来数据
            console.log(response.data); //在控制台中查看数据是否正常返回

            response.data.forEach(function (elem, index, arr) {
                console.log(elem, index);
                option3.series[0].data.push({ 'name': elem.post_province, 'value': parseInt(elem.province_count) })
            });
            myChart3.setOption(option3)

            //{name:'',value:''}
            //=
        })
        .catch(function (error) {
            // 当请求失败的时候，我们如何来处理
            console.log(error);
        })
        .finally(function () {
            // always executed
        });

    // 使用刚指定的配置项和数据显示图表。
    // myChart3.setOption(option3);
    window.addEventListener("resize", function () {
        myChart3.resize();
    });
}


function echarts_4(apiURL) {
    var myChart4 = echarts.init(document.getElementById('echart4'));
    option4 = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    color: '#57617B'
                }
            },
        },

        grid: {
            left: '0',
            right: '20',
            top: '10',
            bottom: '20',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLabel: {
                show: true,
                textStyle: {
                    color: 'rgba(112,166,227,.6)'
                }
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(112,166,227,.6)'
                }
            },
            data: []
        },
        yAxis: [{
            axisLabel: {
                show: true,
                textStyle: {
                    color: 'rgba(112,166,227,.6)'
                }
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(112,166,227,.5)'
                }
            },
            splitLine: {
                lineStyle: {
                    color: 'rgba(112,166,227,.5)'
                }
            }
        }],
        series: [{
            name: '分时段博文数统计（每小时）',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 3
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgba(207,119,192, 0.1)'
                    }, {
                        offset: 1,
                        color: 'rgba(156,136,231, 0.5)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.3)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {
                    color: '#9c88e7',
                    borderColor: 'rgba(207,119,192,0.27)',
                    borderWidth: 12
                }
            },
            data: []
        }]


    };

    axios.get(apiURL)
        .then(function (response) {
            // 当请求成功的时候，response就是后台发送过来数据
            console.log(response.data); //在控制台中查看数据是否正常返回
            timelist = []
            dataList = []
            response.data.forEach(function (elem, index, arr) {
                //console.log(elem, index);
                timelist.push(elem.post_hour)
                dataList.push(parseInt(elem.post_amount))
            });
            console.log(timelist)
            console.log(dataList)
            option4.xAxis.data = timelist
            option4.series[0].data = dataList
            myChart4.setOption(option4);
        })
        .catch(function (error) {
            // 当请求失败的时候，我们如何来处理
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
    // 使用刚指定的配置项和数据显示图表。
    // myChart4.setOption(option4);
    window.addEventListener("resize", function () {
        myChart4.resize();
    });
}

function user_follower(apiURL5) {

    axios.get(apiURL5)
      .then(function (response) { // 当请求成功的时候，response就是后台发送过来数据
        console.log(response.data); //在控制台中查看数据是否正常返回
        response.data.forEach(function (elem, index, arr) {
          console.log(elem, index);
          for (let i = 1; i <= 10; i++) {
            let nid = elem.id % 10 === 0 ? 10 : elem.id % 10;//条件？为真时返回的值：为假时返回的值
            if (nid === i) {
              document.getElementById('f' + i).textContent = elem.username;
              document.getElementById('fc' + i).textContent = elem.user_followers;
              if (Number(elem.user_followers) >= 10000) {
                let followers = Number(elem.user_followers) / 10000;
                document.getElementById('fc' + i).textContent = followers.toFixed(1) + '万';
              }
            }
          }

        });
      })
      .catch(function (error) {
        // 当请求失败的时候，我们如何来处理
        console.log(error);
      })
      .finally(function () {
        // always executed
      });


  }

$(document).ready(function () {

    selectList.addEventListener('change', function() {
        selectedValue = selectList.options[selectList.selectedIndex].value;
        updateAPI(selectedValue);

    });
    // selectList.dispatchEvent(new Event('change'));
});

function updateAPI(selectedValue) {
    // var selectList = document.getElementById("selectList");
    // var selectedValue = selectList.options[selectList.selectedIndex].value;

    var apiURL1 = "http://127.0.0.1:8000/api/user_gender_count/"+ "type" + selectedValue;
    var apiURL2 = "http://127.0.0.1:8000/api/dailyposts/"+ "type" + selectedValue;
    var apiURL3 = "http://127.0.0.1:8000/api/provincecount/"+ "type" + selectedValue;
    var apiURL4 = "http://127.0.0.1:8000/api/hourlyposts/"+ "type" + selectedValue;
    var apiURL5 = "http://127.0.0.1:8000/api/top10f/" + "type" + selectedValue;
    var apiURL6 = "http://127.0.0.1:8000/api/sentimenttime/"+ "type" + selectedValue;

    var img = document.getElementById("myImage");
    img.src = staticUrlforWordcloud+"type" + selectedValue + "_wordcloud.png"+ "?" + version;

    user_follower(apiURL5)

    echarts_1(apiURL1);
    echarts_2(apiURL2);
    echarts_3(apiURL3);
    echarts_4(apiURL4);
    getDataTypeCount(selectedValue);
    echarts_5(apiURL6);
}


// $(function () {
//     updateAPI();
//   });

  $(window).load(function () {
    $(".loading").fadeOut();
  });

  function getDataTypeCount(selectedValue) {
    // var selectList = document.getElementById("selectList");
    
        // var selectedValue = selectList.options[selectList.selectedIndex].value;
        var apiURL = "http://127.0.0.1:8000/api/contentList/count_data_types/";
        axios.get(apiURL)
        .then(function (response) {
            console.log(response.data);
            response.data.forEach(function (elem, index, arr) {
                if(elem.data_type === "type"+selectedValue || selectedValue )
                document.getElementById('datatypeCount').textContent = elem.count + "条";
            });
        })
        .catch(function (error) {
            console.log(error);
        });
    ;
}
// 情感分析散点图
function echarts_5(apiURL) {
    // 基于准备好的dom，初始化echarts实例
    var myChart5 = echarts.init(document.getElementById('echart5'));
    option5 = {
  xAxis: {
    data: []
  },
  yAxis: {},
  tooltip: {
    trigger: 'item',

  },
  series: [
    {
      type: 'scatter',
        symbolSize: 4,
        itemStyle: {
                normal: {
                    color: '#2f89cf',
                }
            },
      data: []
    },


  ]
};

    axios.get(apiURL)
    .then(function (response) {
        // Sort the data array based on the date
        response.data.sort(function (a, b) {
            return new Date(a.post_time) - new Date(b.post_time);
        });

        // Process the sorted data
        var datelist = [];
        var seniList = [];
        response.data.forEach(function (elem) {
            datelist.push(elem.post_time);
            seniList.push(elem.sentiment_indicator);
        });

        // Set the sorted data to the chart option
        option5.xAxis.data = datelist;
        option5.series[0].data = seniList;
        myChart5.setOption(option5);
    })
    .catch(function (error) {
        console.log(error);
    });

    // 使用刚指定的配置项和数据显示图表。
    // myChart5.setOption(option5);
    window.addEventListener("resize", function () {
        myChart5.resize();
    });
}

