//Based on nvd3.js charts objects
//@StanK 20170509
function AuroraChart(options) {
    this.chartType = options.chartType;
    this.view = options.view;
    this.format = options.format;
    this.xAxis = options.xAxis;
    var monthsList = [
    'none',
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
    ];
    this.colorsList = ['rgb(0, 183, 238)', 'rgb(153, 153, 153)', 'rgb(123, 219, 255)'];
    this.colorActive = 'rgb(248, 172, 89)';
    this.filters = {};
    this.dataset = options.dataset
    this.update = function (data, filters) {
        this.filters = filters;
        this.dataset = data;
        chartType = this.chartType
        colorsList = this.colorsList
        colorActive = this.colorActive
            switch (chartType) {
                case 'BarChart':
                    nv.addGraph(function () {
                        var chart = nv.models.multiBarChart()
                        
                            .x(function (d) { return d.label })    //Specify the data accessors.
                            .y(function (d) { return d.value })
                            .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
                            //.rotateLabels(-45)
                            //.showValues(true)       //...instead, show the bar value right on top of each bar.
                            .duration(1000)
                            //.margin({ bottom: 100 })
                            .useInteractiveGuideline(true)
                            .reduceXTicks(false)
                            //.wrapLabels(true)
                            //.barColor(function (d, i) {
                                
                            //    if (options.hasFilter) {
                                   
                            //        if (filters.hasOwnProperty(options.dimension)) {
                                        
                            //            if (filters[options.dimension] === d.label && d.label !== '') {
                            //                return colorActive
                            //            }
                            //            else {
                            //                return colorsList[i]
                            //            }
                            //        }
                            //    }

                            //})
                            .color(function (d, i) {
                            
                                return colorsList[i]
                                
                            })
                            
                            //.valueFormat(d3.format('.2s'))
                        ;
                        //chart.xAxis.rotateLabels(-45)
                        chart.yAxis.tickFormat(d3.format('.2s'))
                        d3.select(options.div)
                            .datum(data)
                            .call(chart);
                        d3.selectAll('.nvtooltip').remove();
                        chart.multibar.dispatch.on(
                            "elementClick",
                            function (e) {
                                if (options.hasFilter) {
                                    ractive.animate('filters.' + options.dimension, e.data.label);
                                }
                            });
                        
                        nv.utils.windowResize(chart.update);

                        return chart;
                    });
                    break;
                case 'PieChart':
                    nv.addGraph(function () {
                        var chart = nv.models.pieChart()
                            .x(function (d) { return d.key })
                            .y(function (d) { return d.value })
                            .showLabels(true)
                            .labelsOutside(true)
                            .donut(true)
                            .color(function (d) {
                                if (options.hasFilter) {
                                    if (filters.hasOwnProperty(options.dimension)) {
                                        if (filters[options.dimension] === d.key) {
                                            return 'rgb(255, 127, 14)'
                                        }
                                        else {
                                            return 'rgb(0, 183, 238)'
                                        }
                                    }
                                    else {
                                        return 'rgb(0, 183, 238)'
                                    }
                                }
                                else {
                                    return 'rgb(0, 183, 238)'
                                }
                            })
                            .showLegend(false);
                        d3.select(options.div)
                            .datum(options.dataset)
                            .call(chart);
                        chart.pie.dispatch.on(
                            "elementClick",
                            function (e) {
                                if (options.hasFilter) {
                                    ractive.animate('filters.' + options.dimension, e.data.key);
                                }
                            });
                        chart
                        return chart;
                    });
                    break;
                case 'StackedAreaChart':
                    nv.addGraph(function () {
                        var chart = nv.models.stackedAreaChart()
                            .x(function (d) { return d[0] })    //Specify the data accessors.
                            .y(function (d) { return d[1] })
                            .duration(1000)
                            .color(this.colors(d))
                           
                            
                        //.valueFormat(d3.format('.2s'))
                        .showLegend(false)
                        .showControls(false)
                        ;
                        //chart.xAxis.rotateLabels(-45)
                        chart.xAxis
                            .tickFormat(function (d) {
                                return d3.time.format('%x')(new Date(d))
                        });
                        chart.yAxis.tickFormat(d3.format(',%'));
                        d3.select(options.div)
                            .datum(data)
                            .call(chart);

                        //chart.discretebar.dispatch.on(
                        //    "elementClick",
                        //    function (e) {
                        //        if (options.hasFilter) {
                        //            ractive.animate('filters.' + options.dimension, e.data.key);
                        //        }
                        //    });
                        nv.utils.windowResize(chart.update);

                        return chart;
                    });
                    break;
                case 'LineChart':
                    nv.addGraph(function () {
                        
                        var chart = nv.models.lineChart()
                                .x(function (d) { return d[0] })    //Specify the data accessors.
                                .y(function (d) { return d[1] })
                                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                                .duration(350)  //how fast do you want the lines to transition?
                                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                                .showYAxis(true)        //Show the y-axis
                                .showXAxis(true)        //Show the x-axis
                                .color(function (d, i) {
                                    
                                    return colorsList[i]
                                })
                                
                        ;
                        if (options.xAxis === 'month') {
                            chart.xAxis.tickFormat(function(d){
                                return monthsList[d];
                            });
                        }
                        else {
                            chart.xAxis
                            .tickFormat(function (d) {
                                return d3.time.format('%x')(new Date(d))
                            });
                        }
                        
                            
                        if (options.yAxis === 'percent') {
                            chart.yAxis.tickFormat(d3.format(',%'));
                        }
                        else {
                            chart.yAxis.tickFormat(d3.format('.2s'))
                        }
                        chart.interactiveLayer.tooltip
                            .gravity('w')
                        ;
                        d3.select(options.div)
                            .datum(data)
                            .call(chart);
                        chart.interactiveLayer.dispatch.on(
                            "elementClick",
                            function (e) {
                                //if (options.hasFilter) {
                                //    ractive.animate('filters.' + options.dimension, e.data.key);
                                //}
                                // console.log(e.pointXValue)
                            });
                        nv.utils.windowResize(chart.update);
                        return chart;
                    });
                    break;
            }
            



    };
    this.update(this.dataset, this.filters);
};

function AuroraKPI(options) {
    this.view = options.view;
    this.value = options.value;
    this.update = function (value) {
        this.value = value;
        return value;
    };
    this.getValue = function () {
        return this.value;
    }
};
function AuroraTable(options) {
    this.view = options.view;
    this.dimensions = options.dimensions;
    this.headers = [];
    this.headers.push(...options.dimensions);
    this.headers.push('Spend', 'Transactions');
    this.columns = [];
    this.columns.push(...options.dimensions);
    this.columns.push('count', 'value');
    this.content = options.content;
    this.update = function (content) {
        this.content = content;
        return content;
    }
}
function AuroraMap(options) {
    this.view = options.view;
    this.dimensions = options.dimensions;
    this.colorsList = ['rgb(0, 183, 238)', 'rgb(153, 153, 153)', 'rgb(123, 219, 255)'];
    this.colorActive = 'rgb(248, 172, 89)';
    //var mapData = {
    //    "US": getRandomInt(50, 800),
    //    "SA": getRandomInt(50, 800),
    //    "DE": getRandomInt(50, 800),
    //    "FR": getRandomInt(50, 800),
    //    "CN": getRandomInt(50, 800),
    //    "AU": getRandomInt(50, 800),
    //    "BR": getRandomInt(50, 800),
    //    "IN": getRandomInt(50, 800),
    //    "GB": getRandomInt(50, 800),
    //    "BE": getRandomInt(50, 800),
    //};

    $(options.div).vectorMap({
        map: 'world_mill_en',
        backgroundColor: "transparent",
        regionStyle: {
            initial: {
                fill: '#e4e4e4',
                "fill-opacity": 0.9,
                stroke: 'none',
                "stroke-width": 0,
                "stroke-opacity": 0
            }

        },

        series: {
            regions: [{
                values: options.data,
                scale: ['rgb(0, 183, 238)', 'rgb(123, 219, 255)'],
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {
            el.html(el.html() + ' (Spend - ' + mapData[code] + ')');
            console.log(mapData[code])
        }
    });
    this.update = function (data) {

    }
}