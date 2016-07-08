var myApp = angular.module('app', ["chart.js"])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    });


myApp.controller("ChartCtrl", function ($scope,$http) {

var getData = function(url) {
$http({
  method: 'GET',
  url: url
}).then(function successCallback(response) {
        $scope.data.push([response.data.measurements.values])
        $scope.labels.push(response.data.measurements.labels)
        $scope.titles.push(url.replace("/api/",""))


  }, function errorCallback(response) {
  });

}

$scope.data = []
$scope.labels = []
$scope.titles = []
$scope.series = ['Sensor'];
$scope.datasetOverride = [{ yAxisID: 'y-axis-1' }];
$scope.options = {
    scales: {
        xAxes: [{
labels: {
    userCallback: function(dataLabel, index) {
        return index % 1 === 0 ? dataLabel : '';
    }
}
}],
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

  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };

getData('/api/Outdoor/Temperature');
getData('/api/GroundFloor/Temperature');
getData('/api/Garage/Temperature');
getData('/api/Outdoor/Humidity');
getData('/api/GroundFloor/Humidity');
getData('/api/Garage/Humidity');

});
