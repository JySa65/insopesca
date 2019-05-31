import Chart from 'chart.js'
import axios from '../../utils/axios'

const $sanidad_home_chart_line = document.querySelector('#sanidad_home_chart_line')
if ($sanidad_home_chart_line) {
    const months = ["ENERO", "FEBRERO", "MARZO", "ABRIL",
        "MAYO", "JUNIO", "JULIO", "AGOSTO",
        "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

    const ctx = $sanidad_home_chart_line.getContext('2d');
    axios.get('/sanidad/api/chart/month/')
        .then(response => {
            const { data } = response
            const datasets = []
            data.forEach((info, index) => {
                const format = {
                    label: info.name,
                    data: info.data,
                    backgroundColor: info.bg,
                    borderColor: info.bd,
                    borderWidth: 1
                }
                datasets.push(format)
            });
            console.log(datasets)
            gChart(datasets)
        })


    const gChart = (datasets) => {
        const year = new Date().getFullYear()
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: months,
                datasets,
            },
            options: {
                // scales: {
                //     xAxes: [{
                //         barPercentage: 0.4,
                //         categoryPercentage: 0.5
                //     }],
                //     yAxes: [{
                //         ticks: {
                //             beginAtZero: false
                //         }
                //     }]
                // },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                responsive: true,
                title: {
                    display: true,
                    text: `Inspecciones ${year}`
                }
            }
        });
    }
}
