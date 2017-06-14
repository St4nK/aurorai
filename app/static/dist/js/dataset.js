// //Based on crossfilter.js
//@StanK 20170509
var DataSet = function (data) {
    this.rawData = crossfilter(data);
    this.dimensions = {};
    this.views = {};
    this.createDimension = function (dimension) {
        if (this.dimensions.hasOwnProperty(dimension)) {
            var tempDim = this.dimensions[dimension]        
        }
        else {
            var tempDim = this.rawData.dimension(function (d) { return d[dimension]; });
            this.dimensions[dimension] = tempDim;
        }
        return dimension
    };
    this.createDimensionMultiple = function (dimensions) {
        if (this.dimensions.hasOwnProperty('multiple')) {
            var tempDim = this.dimensions['multiple']
        }
        else {
            var dimName = 'multiple';
            dimensions.forEach(function (e) {
                dimName = dimName.concat('-' + e);
            });
            var tempDim = this.rawData.dimension(function (d) {
                //stringify() and later, parse() to get keyed objects
                var dimGroup = {};
                dimensions.forEach(function (e) {
                    dimGroup[e] = d[e];
                })
                return JSON.stringify(dimGroup);
            });
            this.dimensions[dimName] = tempDim;
        }
        return dimName
    };
    this.createView = function (dimension, type, on) {
        if (dimension === 'kpi_total') {
            if (type === 'sum') {
                var tempView = this.rawData.groupAll().reduceSum(function (f) { return f[on]; });
            }
            if (type === 'count') {
                var tempView = this.rawData.groupAll().reduceCount(function (f) { return f[on]; });
            }
            this.views['view_' + dimension + '_' + type + '_on_' + on] = tempView;
            return 'view_' + dimension + '_' + type + '_on_' + on
        }
        if (dimension.substring(0, 3) === 'kpi') {
            dimension = dimension.substring(3);
            if (type === 'sum') {
                var tempView = this.bin_counter(this.dimensions[dimension].group())
            }
            if (type === 'count') {
                var tempView = this.dimensions[dimension].groupAll().reduceCount(function (f) { return f[on]; });
            }
            this.views['view_' + dimension + '_' + type + '_on_' + on] = tempView;
            return 'view_' + dimension + '_' + type + '_on_' + on
        }
        else {
            if (type === 'sum') {
                var tempView = this.dimensions[dimension].group().reduceSum(function (f) { return f[on]; });
            }
            if (type === 'count') {
                var tempView = this.dimensions[dimension].group().reduceCount(function (f) { return f[on]; });
            }
            this.views['view_' + dimension + '_' + type + '_on_' + on] = tempView;
            return 'view_' + dimension + '_' + type + '_on_' + on
        }
        
    };
    this.createViewMultiple = function (dimension) {
        var tempView = this.dimensions[dimension].group().reduce(reduceAdd, reduceRemove, reduceInitial).order(orderValue);
        tempView.all().forEach(function (d) {
            d.key = JSON.parse(d.key);
        });
        this.views['view_' + dimension] = tempView;
        return 'view_' + dimension
    };
    this.applyFilter = function (dimension, filters) {
        this.dimensions[dimension].filterExact(filters);
    };
    this.removeFilter = function (dimension) {
        this.dimensions[dimension].filter(null);
    };
    this.returnDataSet = function (view, format) {
        var b = this.views[view].top(20).filter(function (d) { return d.value > 0; });
        if (format === 'multi') {
            return [
                    {
                        key: view,
                        values: b
                    }
            ]
        }
        if (format === 'unique') {
            return b
        }
    };
    this.returnKPI = function (view) {
        return this.views[view].value();
    };
    this.returnTable = function (view, top) {
        return this.views[view].top(top).filter(function (d) { return d.value.count > 0; });
    };
    this.bin_counter =function(group) {
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
};

///////////////////////////////
////// Aurora Dashboard ///////
///////////////////////////////

var AuroraDash = function(options) {
    this.dataset = options.dataset;
    this.charts = {};
    this.kpis = {};
    this.tables = {};
    this.addChart = function (name, chart_type, dimension, sum_count, on, div, hasfilter) {
        mydim = this.dataset.createDimension(dimension);
        myview = this.dataset.createView(mydim, sum_count, on);
        if (chart_type === 'DiscreteBarChart') {
            format = 'multi';
        }
        else {
            format = 'unique';
        }
        mychart = new AuroraChart({
            chartType: chart_type,
            div: div,
            view: myview,
            format: format,
            dataset: this.dataset.returnDataSet(myview, format),
            dimension: dimension,
            hasFilter: hasfilter
        });
        this.charts[name] = mychart;
    };
    this.addKPI = function (name, kpi_type, sum_count, on, format, hasFilter) {
        if (kpi_type === 'total') {
            myview = this.dataset.createView('kpi_total', sum_count, on);
            mykpi = new AuroraKPI({
                view: myview,
                format: format,
                hasFilter: hasFilter,
                value: myds.returnKPI(myview)
            });
        }
        else {
            mydim = this.dataset.createDimension(kpi_type);
            myview = this.dataset.createView('kpi'+ mydim, sum_count, on);
            mykpi = new AuroraKPI({
                view: myview,
                format: format,
                hasFilter: hasFilter,
                value: this.dataset.returnKPI(myview)
            });
        }
        
        this.kpis[name] = mykpi;
    };
    this.addTable = function (name, dimensions, hasFilter) {
        mydim = this.dataset.createDimensionMultiple(dimensions);
        myview = this.dataset.createViewMultiple(mydim);
        mytable = new AuroraTable({
            view: myview,
            dimensions: dimensions,
            hasFilter: hasFilter,
            sum_count:'sum&count',
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
                myds.removeFilter(key);
            }
            else {
                myds.applyFilter(key, dimFilter);
            }
        };
        //refresh the graphs
        for (var key in this.charts) {
            if (this.charts.hasOwnProperty(key)) {
                c = this.charts[key];
                c.update(this.dataset.returnDataSet(c.view, c.format), ractive.get('filters'));
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
                k.update(this.dataset.returnKPI(k.view));
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
    }
    
};