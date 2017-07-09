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

    var getData = function(topic,numdays) {

        var utcOffsetInMinutes = new Date().getTimezoneOffset();
        $http({
            method: 'GET',
            url: "/ChartData/api/" + topic  + "?numdays=" + numdays + "&utcOffset=" + utcOffsetInMinutes
            }).then(function successCallback(response) {
                    values = response.data.measurements.values;
                    labels = response.data.measurements.labels;
                    $scope.data = [values];
                    $scope.labels = labels;
                    title = topic + ": " + lastVal(values,1) + " (" + lastVal(labels,1) + ")";
                    $scope.title = title;


            }, function errorCallback(response) {
        });
    };

    $scope.numdays = 1;

    var getTopics = function() {
        $scope.topics = [
            'Outdoor/Temperature',
            'GroundFloor/Temperature',
            'TopFloor/Temperature',
            'Garden/Temperature',
            'Garage/Temperature',
            'TopFloor/Pressure',
            'Outdoor/Humidity',
            'GroundFloor/Humidity',
            'Garage/Humidity',
            'FrontDoor/Status'
        ];
    };

    $scope.topicChanged = function () {
        requestNewData();
    }

    var requestNewData = function(selectedTopic) {
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

        getData($scope.selectedTopic,$scope.numdays);
    };

    getTopics();
    $scope.selectedTopic = 'Outdoor/Temperature';
    requestNewData();

});
