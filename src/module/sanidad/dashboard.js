import { Calendar } from '@fullcalendar/core';
import interactionPlugin from '@fullcalendar/interaction';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import esLocale from '@fullcalendar/core/locales/es';
import moment from 'moment'
import axios from 'axios'
import swal from 'sweetalert2'

moment.locale('es');

const calendarEl = document.getElementById('calendar');
if (calendarEl) {

    const salert = (pk) => {
        const html = (data) => `
        <p><b>Fecha: </b> ${data.date} </p> 
        <p><b>Proxima: </b> ${data.next_date} </p> 
        <p><b>Resultado: </b> ${data.result == 'is_verygood' ? 'Muy Bueno' : data.result == 'is_good' ? 'Bueno' : 'Malo'} </p> 
        <p><b>Observaciones: </b> ${data.notes} </p> 
        `
        axios.get(`/sanidad/inspection/api/detail/?pk=${pk}`)
        .then(data => {
            const user = data.data
            swal.fire({
                type: 'info',
                title: user.name,
                html: html(user),
            })
        })
    }


    const calendar = new Calendar(calendarEl, {
        locale: esLocale,
        plugins: [interactionPlugin, dayGridPlugin, timeGridPlugin],
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        defaultDate: moment().format('YYYY-MM-DD'),
        navLinks: true, // can click day/week names to navigate views
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        events: (e) => {
            const start = moment(e.start).format('YYYY-MM-DD')
            const end = moment(e.end).format('YYYY-MM-DD')
            return axios.get(`/sanidad/inspection/api/list/?start=${start}&end=${end}`)
            .then(cale => {
                let list_calendar = []
                cale.data.map(data => {
                    const color = data.result == 'is_verygood' ? '#1a252f;' : data.result == 'is_good' ? '#2C3E50' : '#76818d'
                    list_calendar.push({
                        id: data.pk,
                        title: data.name,
                        start: moment(data.next_date).format('YYYY-MM-DD'),
                        backgroundColor: color,
                        borderColor: color,
                        classNames: ['bage_calendar']
                    })
                })
                return list_calendar
            })},
        eventClick: (info) => {
            salert(info.event.id)
            console.log(info.event)
            // alert("hola")
        },
    });
    calendar.render();
}



