var ctx = document.getElementById("classChart").getContext('2d');
var input = $('#classChart').data('chart');

var myChart = new Chart(ctx, {
    type: 'polarArea',
    data: {
        labels: input.labels,
        datasets: [{
            label: 'Probability for each actor',
            data: input.data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Probability of classified actors'
        },
        legend: {
            display: true,
            position: 'bottom'
        }
    }
});