

function createStockChartLastHour(timestamps, highPrices) {

    const ctx = document.getElementById('stockHighChartLastHour').getContext('2d');
    const stockChartLastHour = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps, // X-axis timestamps
            datasets: [{
                label: 'Stock High Prices',
                data: highPrices, // Y-axis high prices
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    type: 'time', // Specify time scale for X-axis
                    time: {
                        unit: 'minute' // Adjust based on the data interval (minute, hour, etc.)
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    title: {
                        display: true,
                        text: 'Stock Price'
                    },
                    beginAtZero: false
                }
            }
        }
    });

    // console.log(timestamps)
}




function createStockChartLastWeek(timestamps, highPrices) {

    const ctx = document.getElementById('stockHighChartLastWeek').getContext('2d');
    const stockChartLastWeek = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps, // X-axis timestamps
            datasets: [{
                label: 'Stock High Prices',
                data: highPrices, // Y-axis high prices
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    type: 'time', // Specify time scale for X-axis
                    time: {
                        unit: 'day',  // The time unit is in minutes (you can adjust as per your need)
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    title: {
                        display: true,
                        text: 'Stock Price'
                    },
                    beginAtZero: false
                }
            }
        }
    });

}


function createStockChartLastYear(timestamps, highPrices) {

    const ctx = document.getElementById('stockHighChartLastYear').getContext('2d');
    const stockChartLastYear = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps, // X-axis timestamps
            datasets: [{
                label: 'Stock High Prices',
                data: highPrices, // Y-axis high prices
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    type: 'time', // Specify time scale for X-axis
                    time: {
                        unit: 'month',  // The time unit is in minutes (you can adjust as per your need)
                    },
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    grid: {
                       color: 'rgba(245, 245, 245, 0.3)'  // Change grid color to whitesmoke
                   },
                    title: {
                        display: true,
                        text: 'Stock Price'
                    },
                    beginAtZero: false
                }
            }
        }
    });

}