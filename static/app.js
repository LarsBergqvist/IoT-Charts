var myApp = angular.module('app', ["chart.js"])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });


myApp.controller("ChartCtrl", function ($scope,$http) {

    var lastVal = function(array, n) {  
    if (array == null)   
        return void 0;  
    if (n == null)   
        return array[array.length - 1];  
    return array.slice(Math.max(array.length - n, 0));    
    };

    var getData = function(url) {
        $http({
            method: 'GET',
            url: url
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

    getData('/api/Outdoor/Temperature');
    getData('/api/GroundFloor/Temperature');
    getData('/api/Garage/Temperature');
    getData('/api/Outdoor/Humidity');
    getData('/api/GroundFloor/Humidity');
    getData('/api/Garage/Humidity');

});
