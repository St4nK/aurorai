// Based on crossfilter.js
// @StanK 20170509
// Amended 20170725

///////////////////
//    Dataset    //
///////////////////

var AuroraData = function (dataset) {
    this.cfData = crossfilter(dataset); // put everything in a crossfilter object
    this.dimensions = {};
    this.views = {};
    this.createDimension = function (dimension) { // function that creates a dimension (which might be multiple columns as one dimension) dimension is an array of columns names in the dataset
        //Generate the name of the dimension to check
        if (dimension.length == 1) { // in case unique dimension
            var DimName = dimension[0];
        }
        else { // in case multiple dimensions
            var DimName = 'multiple';
            dimension.forEach(function (e) {
                DimName = DimName.concat('__' + e);
            });
        }

        if (this.dimensions.hasOwnProperty(DimName)) { // if dimension name exists, do nothing (to not overcreate dimensions)
            var tempDim = this.dimensions[DimName];
        }
        else {
            if (dimension.length === 1) {
                var tempDim = this.cfData.dimension(function (d) { return d[dimension]; });
            }
            else {
                var tempDim = this.cfData.dimension(function (d) {
                    //stringify() and later, parse() to get keyed objects
                    var dimGroup = {};
                    dimension.forEach(function (e) {
                        dimGroup[e] = d[e];

                    })
                    
                    return JSON.stringify(dimGroup);
                });
               
            }
            this.dimensions[DimName] = tempDim;
        }
        return DimName
    };

    this.createView = function (options) {
        
        if (this.views.hasOwnProperty(options.name)) { // in case the view already exists
            return options.name
        }
        
        else {
            if (options.format.type === 'series') { // adding the series dimension to the list of dimensions
                options.dimension.push(options.format.dimension)
            }
            // 1. In case this is a global KPI, meaning not linked to a certain dimension
            if (typeof options.filterLocal === 'undefined' && options.type === 'kpi') {
                if (typeof options.sum != 'undefined') {
                    var tempView = this.cfData.groupAll().reduceSum(function (f) { return f[options.sum]; }); // sum on the field provided
                }
                else if (typeof options.count != 'undefined') {
                    var tempView = this.rawData.groupAll().reduceCount(function (f) { return f[options.count]; }); // count on the field provided
                }
                
            }
            // 2. in case this is a dimension related KPI, it could be a count of unique values, or a filterLocal on this specific dimension (e.g. {dimension:Scenario, value:Budget} )
            else if (options.type === 'kpi') {
                if (typeof options.count !== 'undefined') {
                    tempDim = this.createDimension(options.dimension); //create the dimension
                    var tempView = this.unique_counter(this.dimensions[tempDim].group()); // see helpsrs for the unique_counter function
                }
                else if (typeof options.filterLocal !== 'undefined' && typeof options.sum !== 'undefined') {
                    tempDim = this.createDimension([options.filterLocal[0].dimension]); //create the dimension
                    
                    var tempView = this.dimensions[tempDim].group().reduceSum(function (f) {
                        return f[options.sum];
                    });
                }
                else {
                    console.log('dimension could not be created')
                    return
                }

            }
            // 3. in case this is a chart/table unique dimension
            else if (options.dimension.length === 1 && options.type !=='table') {
                tempDim = this.createDimension(options.dimension); //create the dimension
                
                if (typeof options.sum != 'undefined') {
                    var tempView = this.dimensions[tempDim].group().reduceSum(function (f) { return f[options.sum]; });
                }
                else if (typeof options.count != 'undefined') {
                    var tempView = this.dimensions[tempDim].group().reduceCount(function (f) { return f[options.count]; });
                }
                else {
                    console.log('dimension could not be created')
                    return
                }
            }
            // 4. in case this is a multiple dimension
            else if (options.dimension.length > 1 ||  options.type === 'table') {
                uniqueDim = this.createDimension([options.dimension[0]]); //Create the unique dimension to 
                tempDim = this.createDimension(options.dimension); //create the multiple dimension
                var tempView = this.dimensions[tempDim].group().reduce(reduceAdd, reduceRemove, reduceInitial).order(orderValue); // see helpers for the reduce functions
            }
            // 5. Oops something went wrong
            else {
                console.log('Ooops, dimension could not be created')
                return
            }
        }
        var viewObject = {
            view: tempView,
            dimension: options.dimension,
            sum: options.sum,
            count: options.count,
            filterLocal: options.filterLocal,
            type: options.type,
            format: options.format,
            topnum: options.topnum,
            chartType: options.chartType
        };
        
        this.views[options.name] = viewObject; // saving the viewObject by its name
        return options.name
    };

    ////////////
    // Functions
    ////////////

    this.applyFilter = function (dimName, filters) {
        this.dimensions[dimName].filterExact(filters);
    };
    this.removeFilter = function (dimName) {
        this.dimensions[dimName].filter(null);
    };


    this.returnData = function (viewName) {
        viewObject = this.views[viewName]; // retrieve the view/group of the viewObject

        //return the chart type of data
        if (viewObject.type === 'chart') {
            if (typeof viewObject.topnum === 'undefined') { // if top is not defined, put it to Infinity
                viewObject.topnum = Infinity;
            }

            var tempData = viewObject.view.top(viewObject.topnum);//.filter(function (d) { return d.value !== 0; })

            //filter Local if exists
            if (typeof viewObject.filterLocal !== 'undefined') {
                viewObject.filterLocal.forEach(function (filterObj) {
                    tempData = tempData.filter(function (d) {
                        return filterObj.values.includes(d[filterObj.dimension])
                    });
                });
            }
            //render the dataset to be consumed by the chart lib
            if (typeof viewObject.format !== 'undefined') {
                //split the data in series in case this is the format

                if (viewObject.format.type === 'series') {
                    var series = [];
                    viewObject.format.values.forEach(function (e) {
                        series.push({ key: e, values: [] })
                    })
                    var dim = viewObject.format.dimension;
                    tempData.forEach(function (d) {
                        var newKey = JSON.parse(d.key);//parse the data
                        series.forEach(function (s) {
                            if (newKey[dim] === s.key) {
                                delete newKey[dim];
                                s.values.push({ label: newKey[Object.keys(newKey)[0]], value: d.value.value });
                            }
                        })
                    })
                    // In case of LineChart, rearranging asc by label value (considered to be int)
                    if (viewObject.chartType === 'LineChart') {
                        var serie0labels = series[0].values.map(function (a) { return a.label });
                        serie0labels.sort(function (a, b) {
                            return parseInt(a) - parseInt(b);
                        });
                    }
                        //Need to rearrange arrays to have labels in the same order, taking serie 0 as basis
                    else {
                        var serie0labels = series[0].values.map(function (a) { return a.label; });
                    }
                    // Rearranging
                    series.forEach(function (s) {
                        s.values = rearrange(s.values, 'label', serie0labels);
                    });
                    // Linearising values for LineChart
                    if (viewObject.chartType === 'LineChart') {
                        series.forEach(function (s) {
                            s.values = linearise(s.values)
                        })
                    }
                    console.log(series)
                    return series
                }
                if (viewObject.format.type === 'multi') {
                    var finalData = [];
                    tempData.forEach(function (d) {
                        finalData.push({ label: d.key, value: d.value });
                        //d.values = {label:d.values.key, value:d.value.value}

                    })
                   
                    return [
                        {
                            key: viewObject.dimension[0],
                            values: finalData
                        }
                    ]
                }
            }
        }
        else if (viewObject.type === 'kpi') {
            //filter Local if exists
            if (typeof viewObject.filterLocal !== 'undefined') {
                var tempData = viewObject.view.top(Infinity);
                viewObject.filterLocal.forEach(function (filterObj) {
                    tempData = tempData.filter(function (d) {
                        return filterObj.values.includes(d.key)
                    });
                });
                return tempData[0].value;
            }
            else {

                return viewObject.view.value();
            }
            
        }
        else if (viewObject.type === 'table') {
            return viewObject.view.top(viewObject.topnum).filter(function (d) { return d.value.count > 0; });
        }
    }

    ////////////
    //helpers
    this.unique_counter = function (group) { //used in the KPI count of unique values view
        return {
            value: function () {
                return group.all().filter(function (kv) {
                    return kv.value > 0;
                }).length;
            }
        };
    }
    function reduceInitial() {
        return {
            value: 0,
            count: 0
        };
    }
    function reduceAdd(p, v) {
        p.value = p.value + v.value;
        p.count = p.count + v.count;
        return p;
    }
    function reduceRemove(p, v) {
        p.value = p.value - v.value;
        p.count = p.count - v.count;
        return p;
    }
    function orderValue(p) {
        return p.value;
    }
    function rearrange(series, key, keysList) { //function used to rearrange all series according to the same keysList to draw the series graphs proprely
        var tempS = [];
        keysList.forEach(function (k) {
            series.forEach(function (s) {
                if (s[key] === k) {
                    tempS.push(s)
                }
            });
        });
        return tempS
    }
    function linearise(series) { //function used by graphs where [x,y] couples are needed instead of Objects
        var tempS = [];
        series.forEach(function (s) {
            tempS.push([parseInt(s.label), s.value])
        });
        return tempS
    }
    this.returnTable = function (view, top) {
        console.log(view)
        return this.views[view].view.top(top).filter(function (d) { return d.value.count > 0; });
    };
};


///////////////////////////////
////// Aurora Dashboard ///////
///////////////////////////////

var AuroraDash = function (options) {
    this.dataset = {};
    this.charts = {};
    this.kpis = {};
    this.tables = {};
    this.addDataSet = function (dataset) {
        this.dataset = dataset;
        return true
    };

    this.addChart = function (options) {
        var options_view = {
            name:'view_' + options.name,
            dimension: options.dimension,
            sum: options.sum,
            count: options.count,
            filterLocal: options.filterLocal,
            type: 'chart',
            format: options.format,
            topnum: options.topnum,
            chartType: options.chartType
        }
        var chartType = options.chartType;
        var div = options.div;
        var hasFilter = options.hasFilter;
        myview = this.dataset.createView(options_view);
        mychart = new AuroraChart({
            chartType: chartType,
            div: div,
            view: myview,
            xAxis: 'month',
            dataset: this.dataset.returnData(myview),
            dimension: options.dimension[0],
            hasFilter: hasFilter
        });
        this.charts[options.name] = mychart;
    };
    this.addKPI = function (options) {
        var options_view = {
            name: 'view_' + options.name,
            dimension: options.dimension,
            sum: options.sum,
            count: options.count,
            filterLocal: options.filterLocal,
            type: options.type,
            format: options.format,
            topnum: options.topnum,
        }
        myview = this.dataset.createView(options_view);
        mykpi = new AuroraKPI({
            view: myview,
            value: this.dataset.returnData(myview)
        });

        this.kpis[options.name] = mykpi;
    };
    //TODO change to new options format
    this.addTable = function (name, dimensions, hasFilter) {
        var options_view = {
            name: 'view_table',
            dimension: dimensions,
            type: 'table',
            format: { type: 'multi'},
        }
        myview = this.dataset.createView(options_view);
        mytable = new AuroraTable({
            view: myview,
            dimensions: dimensions,
            hasFilter: hasFilter,
            sum_count: 'sum&count',
            content: this.dataset.returnTable(myview, 20)
        });
        this.tables[name] = mytable;
    };

    this.refreshData = function (ractive) {
        //apply the filters
        for (var key in ractive.get('filters')) {
            var dimFilter = ractive.get('filters.' + key);
            if (dimFilter === '') {
                //No filters applied
                this.dataset.removeFilter(key);
            }
            else {
                this.dataset.applyFilter(key, dimFilter);
            }
        };
        //refresh the graphs
        for (var key in this.charts) {
            if (this.charts.hasOwnProperty(key)) {
                c = this.charts[key];
                
                c.update(this.dataset.returnData(c.view), ractive.get('filters'));
            }
        };
        ractive.animate('kpiValuesList', this.kpiValues())
        ractive.animate('tables', this.refreshTables())
    };
    this.kpiValues = function () {
        var kpiValuesList = {};
        for (var key in this.kpis) {
            if (this.kpis.hasOwnProperty(key)) {
                k = this.kpis[key];
                k.update(this.dataset.returnData(k.view));
                kpiValuesList[key] = k.value
            }
        };
        return kpiValuesList;
    };
    this.refreshTables = function () {
        for (var key in this.tables) {
            if (this.tables.hasOwnProperty(key)) {
                t = this.tables[key];
                t.update(this.dataset.returnTable(t.view, 20));
            }
        };
        return this.tables;
    };
    
    this.setRactive = function (ractive) {
        ractive.set('myDash', this);
        ractive.set('kpiValuesListStick', this.kpiValues());
        ractive.set('kpiValuesList', this.kpiValues());
        ractive.set('tables', this.refreshTables());
        ractive.set('loading_data', false);
    }

};