import moment from 'moment'
import swal from 'sweetalert2'
import axios from '../../utils/axios'

const form_report_sanidad = document.querySelector("#form_report_sanidad")
if (form_report_sanidad) {
    const state = {
        type_company: '',
        company: '',
        week1: '',
        week2: '',
        date: 0
    }
    const date = new Date().getFullYear();
    const endDate = new Date(date + 1, 1, 1)
    const startDate = new Date(date - 100, 1, 1)

    const $id_type_company = document.querySelector("#id_type_company")
    const $id_company = document.querySelector("#id_company")
    // const $id_date_range1 = document.querySelector("#id_date_range1")
    // const $id_date_range2 = document.querySelector("#id_date_range2")
    // const $id_date_range1_text = document.querySelector("#id_date_range1_text")
    // const $id_date_range2_text = document.querySelector("#id_date_range2_text")

    const onChange = (e) => {
        state[e.target.name] = e.target.value
    }

    $id_company.addEventListener('change', e => onChange(e))
    $id_type_company.addEventListener('change', e => onChange(e))

    $('#id_date_range1').datepicker({
        language: 'es',
        title: "Insopesca",
        autoclose: true,
        endDate,
        startDate,
        calendarWeeks: true,
        weekStart: 1,
        clearBtn: true
    });
    $('#id_date_range1').on('changeDate', e => {
        const year = moment(e.date).format('YYYY');
        const week = moment(e.date).format('WW');
        const value = `${year}-${week}`
        state.week1 = value
        document.querySelector(`#id_date_range1_text`).value = value
        document.querySelector('#id_date_range2').value = ''
        document.querySelector(`#id_date_range2_text`).value = ''
        changeDate2(e.date)
    });


    const changeDate2 = date => {
        $('#id_date_range2').datepicker({
            language: 'es',
            title: "Insopesca",
            autoclose: true,
            endDate,
            calendarWeeks: true,
            weekStart: 1,
            clearBtn: true
        }).on('changeDate', e => {
            const year = moment(e.date).format('YYYY');
            const week = moment(e.date).format('WW');
            const value = `${year}-${week}`
            state.week2 = value
            document.querySelector(`#id_date_range2_text`).value = value
        });
        $('#id_date_range2').datepicker('setStartDate', date)
    }

    const changeSelect = (value, id_attr) => {
        id_attr.value = ""
        if (value != "") {
            id_attr.setAttribute('disabled', 'disabled')
        } else {
            id_attr.removeAttribute('disabled')
        }

    }

    $id_type_company.addEventListener('change',
        e => changeSelect(e.target.value, $id_company))
    $id_company.addEventListener('change',
        e => changeSelect(e.target.value, $id_type_company))

    form_report_sanidad.addEventListener('submit', e => {
        e.preventDefault()
        const { type_company, company, week1, week2 } = state

        if (type_company == "" && company == "" ||
            type_company != "" && company != "") {
            swal.fire('Debes Escoger una compañia o un tipo de compañia', '', 'warning')
            return false
        }

        swal.fire({
            type: 'warning',
            title: 'Desea Hacer La Consulta con la fecha',
            showCancelButton: true,
            cancelButtonText: 'No',
            confirmButtonText: 'Si',
            toast: true

        }).then(bool => {
            if (bool.value) {
                if (week1 == "" && week2 != "" || week1 == "" && week2 == "") {
                    swal.fire('Asignes Fecha Inicial Para La Consulta', '', 'warning')
                    return false
                }
                if (week2 == "") {
                    const week = state.week1
                    state.week2 = `${week.split('-')[0]}-52`
                }
                state.date = 1
            } else {
                state.date = 0
            }
            axios.get(`/sanidad/api/report/?type_company=${type_company}&company=${company}&week1=${week1}&week2=${state.week2}&date=${state.date}`)
                .then(response => {
                    const { data } = response
                    console.log(data)
                })
        })
    })

}

