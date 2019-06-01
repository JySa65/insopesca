import moment from 'moment'
import swal from 'sweetalert2'
import axios from '../../utils/axios'
import empty from 'empty-element'
import template from './report_view_template'
import t_inspection from './report_view_inspection'
import yo from 'yo-yo'

const form_report_sanidad = document.querySelector("#form_report_sanidad")
if (form_report_sanidad) {
    const state = {
        type_company: '',
        company: '',
        driver: '',
        week1: '',
        week2: '',
        date: 0
    }
    const date = new Date().getFullYear();
    const endDate = new Date(date + 1, 1, 1)
    const startDate = new Date(date - 100, 1, 1)

    const $id_type_company = document.querySelector("#id_type_company")
    const $id_company = document.querySelector("#id_company")
    const $id_driver = document.querySelector("#id_driver")

    const onChange = (e) => {
        state[e.target.name] = e.target.value
    }

    $id_type_company.addEventListener('change', e => onChange(e))
    $id_company.addEventListener('change', e => onChange(e))
    $id_driver.addEventListener('change', e => onChange(e))

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
        state.week2 = `${year}-52`
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
        id_attr.forEach(data => {
            data.value = ""
            if (value != "") {
                data.setAttribute('disabled', 'disabled')
            } else {
                data.removeAttribute('disabled')
            }
        })
    }

    $id_type_company.addEventListener('change',
        e => changeSelect(e.target.value, [$id_company, $id_driver]))
    $id_company.addEventListener('change',
        e => changeSelect(e.target.value, [$id_type_company, $id_driver]))
    $id_driver.addEventListener('change',
        e => changeSelect(e.target.value, [$id_type_company, $id_company]))

    form_report_sanidad.addEventListener('submit', e => {
        e.preventDefault()
        const { type_company, company, driver, week1, week2 } = state

        if (type_company == "" && company == "" && driver == "" ||
            type_company != "" && company != "" && driver != "") {
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
            axios.get(`/sanidad/api/report/?type_company=${type_company}&company=${company}&driver=${driver}&week1=${week1}&week2=${state.week2}&date=${state.date}`)
                .then(response => {
                    const el = document.querySelector("#reports_view_id")
                    const { data } = response
                    const emp = empty(el)
                    if (data.status != false) {
                        data.forEach((data, index) => {
                            emp.append(template(data, index))
                        });
                        const html = data.length != 0 ? yo`
                        <div class="row mt-5">
                            <div class="col-sm-12 text-center">
                                <a href="/reports/sanidad/inspection/?type_company=${type_company}&company=${company}&driver=${driver}&week1=${week1}&week2=${state.week2}&date=${state.date}" class="btn btn-lg btn-success" target="_blank">
                                    <i class="far fa-file-pdf"></i>
                                    Generar PDF
                                </a>
                            </div>
                        </div>                        
                        ` : yo`
                            <div class="row">
                                <div class="col-12 text-center">
                                    <label class="h1">No Hay Inspecciones Vencidas</label>
                                </div>
                            </div>
                        `
                        emp.append(html)
                    } else {
                        swal.fire(`${data.msg}`, '', 'error')
                    }
                })
        })
    })

}

const $report_sanidad_expired = document.querySelector("#form_report_sanidad_expired")
if ($report_sanidad_expired) {
    $report_sanidad_expired.addEventListener('submit', e => {
        e.preventDefault()
        axios.get('/sanidad/api/report/inspections')
        .then(data => {
            const el = document.querySelector("#reports_view_id")
            empty(el).append(t_inspection(data.data))
        })
    })
}
