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
    this.filters = {};
    this.dataset = options.dataset
    this.update = function (data, filters) {
        this.filters = filters;
        this.dataset = data;
        chartType = this.chartType
        
            switch (chartType) {
                case 'DiscreteBarChart':
                    nv.addGraph(function () {
                        var chart = nv.models.discreteBarChart()
                            .x(function (d) { return d.key })    //Specify the data accessors.
                            .y(function (d) { return d.value })
                            .staggerLabels(false)    //Too many bars and not enough room? Try staggering labels.
                            .showValues(true)       //...instead, show the bar value right on top of each bar.
                            .duration(1000)
                            .margin({ bottom: 100 })
                            .color(function (d) {
                                if (options.hasFilter) {
                                    if (filters.hasOwnProperty(options.dimension)) {
                                        if (filters[options.dimension] === d.key && d.key !=='') {
                                            return 'rgb(248, 172, 89)'
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
                            .valueFormat(d3.format('.2s'))
                        ;
                        chart.xAxis.rotateLabels(-45)
                        chart.yAxis.tickFormat(d3.format('.2s'))
                        d3.select(options.div)
                            .datum(data)
                            .call(chart);

                        chart.discretebar.dispatch.on(
                            "elementClick",
                            function (e) {
                                if (options.hasFilter) {
                                    ractive.animate('filters.' + options.dimension, e.data.key);
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
                                .showLegend(false)       //Show the legend, allowing users to turn on/off line series.
                                .showYAxis(true)        //Show the y-axis
                                .showXAxis(true)        //Show the x-axis
                                
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
                            chart.yAxis.tickFormat(d3.format('.1f'));
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
                                console.log(e.pointXValue)
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
    this.format = options.format;
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