import Chart from 'chart.js'
import axios from '../../utils/axios'

const color = {
    bd_primary: '#3b98da',
    primary: '#007bff',
    bd_success: '#01751b',
    success: '#28a745',
    bd_danger: '#73000b',
    danger: '#dc3545'
}

const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

const $sanidad_home_chart_line = document.querySelector('#sanidad_home_chart_line')
if ($sanidad_home_chart_line) {
    const $selectChartYearChange = document.querySelector('#id_select_chart_year_change')
    if ($selectChartYearChange) {
        $selectChartYearChange.addEventListener('change', e => {
            e.preventDefault()
            render(e.target.value)
        })
    }

    const months = ["ENERO", "FEBRERO", "MARZO", "ABRIL",
        "MAYO", "JUNIO", "JULIO", "AGOSTO",
        "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

    const render = (year = new Date().getFullYear()) => {
        const ctx = $sanidad_home_chart_line.getContext('2d');
        axios.get(`/api/sanidad/chart_month/?year=${year}`)
            .then(response => {
                const { data } = response
                const datasets = []
                data.forEach(info => {
                    const format = {
                        label: info.name,
                        data: info.data,
                        backgroundColor: info.bg,
                        borderColor: info.bd,
                        borderWidth: 1
                    }
                    datasets.push(format)
                });
                gChart(datasets, ctx, year)
            })
    }

    render()

    const gChart = (datasets, ctx, year) => new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets,
        },
        options: {
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
                text: `Total De Inspecciones Por Mes Del Año ${year}`,
                fontSize: 24,
                fontColor: '#5969ff',
                lineHeight: 2
            }
        }
    });
}

const $sanidad_home_chart_pie = document.querySelector('#sanidad_home_chart_pie')
if ($sanidad_home_chart_pie) {
    const getData = (year) => axios.get(
        `/api/sanidad/chart_inspection_driver_company/?year=${year}`)

    const gChart = data => new Chart(sanidad_home_chart_pie, {
        type: 'pie',
        data: {
            labels: [data[0].name, data[1].name],
            datasets: [{
                label: '# De Conductores y Compañias',
                data: [data[0].data, data[1].data],
                backgroundColor: [
                    color.primary,
                    color.success,
                ],
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: `Total De Inspecciones Compañia y Conductor`,
                fontSize: 18,
                fontColor: '#5969ff',
                lineHeight: 2
            }
        }
    });

    const render = (year = new Date().getFullYear()) => {
        getData(year).then(({ data }) => {
            gChart(data)
        })
    }
    render()
}

const $sanidad_home_chart_pie1 = document.querySelector('#sanidad_home_chart_pie1')
if ($sanidad_home_chart_pie1) {
    const getData = (year) => axios.get(
        `/api/sanidad/chart_inspection_type/?year=${year}`)

    const gChart = data => new Chart(sanidad_home_chart_pie1, {
        type: 'pie',
        data: {
            labels: data.name,
            datasets: [{
                label: '# Inspecciones Por Tipo',
                data: data.data,
                backgroundColor: data.colors,
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: `Total De Inspecciones Por Tipo`,
                fontSize: 18,
                fontColor: '#5969ff',
                lineHeight: 2
            }
        }
    }).update();
    const render = (year = new Date().getFullYear()) => {
        const getColors = (num) => {
            const colors = []
            for (let i = 0; i < num; i++) {
                const color = getRandomColor()
                colors.push(color)
            }
            return colors
        }
        getData(year).then(({ data }) => {
            const colors = getColors(data.name.length)
            data.colors = colors
            gChart(data)
        })
    }
    render()
}

