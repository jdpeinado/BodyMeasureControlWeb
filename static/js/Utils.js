
Array.prototype.max = function () {
    return Math.max.apply(null, this);
};
Array.prototype.min = function () {
    return Math.min.apply(null, this);
};

var bwChartCtx = document.getElementById('bwChart');
bdMax = bdData.max() + 20 / 100;
bdMin = bdData.min() - 20 / 100;
var bwChart = new Chart(bwChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: bdData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint

            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: bdMin,
                    suggestedMax: bdMax
                }
            }]
        },

        elements: elements

    }
});

var chestChartCtx = document.getElementById('chestChart');
chestMax = chestData.max() + 20 / 100;
chestMin = chestData.min() - 20 / 100;
var chestChart = new Chart(chestChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: chestData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint
            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: chestMin,
                    suggestedMax: chestMax
                }
            }]
        },
        elements: elements
    }
});
var waistChartCtx = document.getElementById('waistChart');
waistMax = waistData.max() + 20 / 100;
waistMin = waistData.min() - 20 / 100;
var waistChart = new Chart(waistChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: waistData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint
            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: waistMin,
                    suggestedMax: waistMax
                }
            }]
        },
        elements: elements
    }
});
var hipChartCtx = document.getElementById('hipChart');
hipMax = hipData.max() + 20 / 100;
hipMin = hipData.min() - 20 / 100;
var hipChart = new Chart(hipChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: hipData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint
            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: hipMin,
                    suggestedMax: hipMax
                }
            }]
        },
        elements: elements
    }
});
var legChartCtx = document.getElementById('legChart');
legMax = legData.max() + 20 / 100;
legMin = legData.min() - 20 / 100;
var legChart = new Chart(legChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: legData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint
            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: legMin,
                    suggestedMax: legMax
                }
            }]
        },
        elements: elements
    }
});
var bicepChartCtx = document.getElementById('bicepChart');
bicepMax = bicepData.max() + 20 / 100;
bicepMin = bicepData.min() - 20 / 100;
var bicepChart = new Chart(bicepChartCtx, {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', ''],
        datasets: [{
            label: '',
            backgroundColor: 'transparent',
            pointBackgroundColor: ['#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1', '#0d47a1'],
            borderColor: '#0d47a1',
            data: bicepData
        }]
    },

    options: {
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                display: false,
                offset: onePoint
            }],
            yAxes: [{
                display: false,
                ticks: {
                    suggestedMin: bicepMin,
                    suggestedMax: bicepMax
                }
            }]
        },
        elements: elements
    }
});
