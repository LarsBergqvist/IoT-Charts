var myApp = angular.module('app', ["chart.js"])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });


myApp.controller("ChartCtrl", function ($scope,$http) {

    $scope.numdaysChanged = function() {
        requestNewData();
    };

    var lastVal = function(array, n) {  
        if (array == null)   
            return void 0;  
        if (n == null)   
            return array[array.length - 1];  
        return array.slice(Math.max(array.length - n, 0));    
    };

    var getData = function(url,numdays) {
        $http({
            method: 'GET',
            url: url + "/" + numdays
            }).then(function successCallback(response) {
                    values = response.data.measurements.values;
                    labels = response.data.measurements.labels;
                    $scope.data.push([values]);
                    $scope.labels.push(labels);
                    title = url.replace("/api/","") + ": " + lastVal(values,1) + " (" + lastVal(labels,1) + ")";
                    $scope.titles.push(title);


            }, function errorCallback(response) {
        });
    };

    $scope.numdays = 1;

    var requestNewData = function() {
        $scope.data = [];
        $scope.labels = [];
        $scope.titles = [];
        $scope.series = ['Sensor'];
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }];
        $scope.options = {
            scales: {
                yAxes: [
                    {
                    id: 'y-axis-1',
                    type: 'linear',
                    display: true,
                    position: 'left'
                    }
                ]
            }
        };

        getData('/api/Outdoor/Temperature',$scope.numdays);
        getData('/api/GroundFloor/Temperature',$scope.numdays);
        getData('/api/Garage/Temperature',$scope.numdays);
        getData('/api/Outdoor/Humidity',$scope.numdays);
        getData('/api/GroundFloor/Humidity',$scope.numdays);
        getData('/api/Garage/Humidity',$scope.numdays);
    };

    requestNewData();

});
