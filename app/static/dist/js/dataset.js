// //Based on crossfilter.js
//@StanK 20170509
var DataSet = function (data) {
    this.rawData = crossfilter(data);
    this.dimensions = {};
    this.views = {};
    this.createDimension = function (dimension) {
        var tempDim = this.rawData.dimension(function (d) { return d[dimension]; });
        this.dimensions[dimension] = tempDim;
        return dimension
    };
    this.createView = function (dimension, type, on) {
        if (dimension === 'kpi') {
            if (type === 'sum') {
                var tempView = this.rawData.groupAll().reduceSum(function (f) { return f[on]; });
            }
            if (type === 'count') {
                var tempView = this.rawData.groupAll().reduceCount(function (f) { return f[on]; });
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
        console.log(this.views[view].value())
    };
};