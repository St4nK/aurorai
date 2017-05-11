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
        if (type === 'sum') {
            var tempView = this.dimensions[dimension].group().reduceSum(function (f) { return f[on]; });
            this.views['view_' + dimension + '_' + type + '_on_' + on] = tempView;
        }
        return 'view_' + dimension + '_' + type + '_on_' + on
    };
    this.applyFilter = function (dimension, filters) {
        this.dimensions[dimension].filterExact(filters);
    };
    this.removeFilter = function (dimension) {
        this.dimensions[dimension].filter(null);
    };
    this.returnDataSet = function (view, format) {
        var b = this.views[view].top(Infinity).filter(function (d) { return d.value > 0; });
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
};