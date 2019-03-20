import { Calendar } from '@fullcalendar/core';
import interactionPlugin from '@fullcalendar/interaction';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import esLocale from '@fullcalendar/core/locales/es';
import moment from 'moment'
import axios from 'axios'

moment.locale('es');

const calendarEl = document.getElementById('calendar');
if (calendarEl) {

    const calendar = new Calendar(calendarEl, {
        locale: esLocale,
        plugins: [interactionPlugin, dayGridPlugin, timeGridPlugin],
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        defaultDate: new Date(),
        navLinks: true, // can click day/week names to navigate views
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        events: () => axios.get('/sanidad/inspection/api/list')
            .then(cale => {
                let list_calendar = []
                cale.data.map(data => {
                    list_calendar.push({
                        id: data.pk,
                        title: data.name,
                        start: new Date(data.next_date),
                        backgroundColor: 'green' 
                    })
                    console.log(data)
                })
                return list_calendar
            }),
        eventClick: (info) => {
            console.log(info)
            // alert("hola")
        },
    });
    calendar.render();
}



