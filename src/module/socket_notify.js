import swal from 'sweetalert2';
import axios from '../utils/axios';
import getCookie from '../utils/get_cookie';
import { format, register } from 'timeago.js';
import es from 'timeago.js/lib/lang/es';
import empty from 'empty-element';
import yo from 'yo-yo';

const socket = new WebSocket(
    `ws://${window.location.host}/ws/notify/`);

socket.onclose = (e) => {
    console.log('notify socket closed unexpectedly');
};

socket.onopen = () => {
    console.log("Connected to notify socket room");
};
socket.addEventListener('message', (e) => {
    // console.log('Message from server', event);
    const backUp = document.querySelector("#backup")
    if (backUp) backUp.removeAttribute('disabled')
    const data = JSON.parse(e.data)
    swal.fire(data.msg, '', 'success')
});

const config = {
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
    }
}
const backUp = document.querySelector("#backup")
if (backUp) {
    backUp.addEventListener('click', () => {
        backUp.setAttribute('disabled', 'disabled')
        swal.fire({
            type: "warning",
            titleText: "¿Esta Seguro De Respaldar La Base de Datos?",
            showCancelButton: true,
            cancelButtonText: 'No',
            showConfirmButton: true,
            confirmButtonText: 'Si',
            allowOutsideClick: false,
            allowEnterKey: false,
            allowEscapeKey: false,
        }).then(data => {
            if (data.value) {
                axios.post('authentication/bd/', {}, config).then(data => {
                    const { status, msg } = data.data
                    if (status) swal.fire(msg, '', 'info')
                })
            } else {
                backUp.removeAttribute('disabled')
            }
        })
    })
}

const restore = e => {
    document.querySelector("#togle_table").setAttribute('hidden', 'hidden')
    empty(document.querySelector('#table_show_db'))
    restoreDB.removeAttribute('disabled')
    swal.fire({
        type: "warning",
        titleText: "¿Esta Seguro De Restaurar La Base de Datos a este tiempo?",
        showCancelButton: true,
        cancelButtonText: 'No',
        showConfirmButton: true,
        confirmButtonText: 'Si',
        allowOutsideClick: false,
        allowEnterKey: false,
        allowEscapeKey: false,
    }).then(data => {
        if (data.value) {
            axios.post('authentication/api/bd/', { id: e.target.id }, config).then(data => {
                const { status, msg } = data.data
                if (status) {
                    swal.fire({
                        type: "info",
                        titleText: msg,
                        showCancelButton: false,
                        showConfirmButton: false,
                        allowOutsideClick: false,
                        allowEnterKey: false,
                        allowEscapeKey: false,
                        onBeforeOpen: () => {
                            // Swal.showLoading()
                            swal.showLoading()
                        },
                    })
                }
            })
        } else {
            backUp.removeAttribute('disabled')
        }
    })
}

const restoreDB = document.querySelector("#restore_db")
const removeCard = document.querySelector("#remove_card")

if (restoreDB) {
    restoreDB.addEventListener('click', () => {
        axios.get('authentication/api/bd/')
            .then(data => {
                const table = document.querySelector('#table_show_db')
                document.querySelector("#togle_table").removeAttribute('hidden')
                if (data.data.length == 0) {
                    let emt = empty(table)
                    let html = yo`
                        <tr>
                            <td>No Tiene</td>
                            <td>Registrado ningun</td>
                            <td>Respaldo de Base de Datos</td>
                        </tr>
                    `
                    return emt.append(html)
                }
                restoreDB.setAttribute('disabled', 'disabled')
                register('es', es);
                let emt = empty(table)
                data.data.forEach((db, i) => {
                    emt.append(yo`
                        <tr>
                            <td>${i + 1}</td>
                            <td>${format(db.fields.created_at, 'es')}</td>
                            <td>
                                <button class="btn btn-lg btn-success" data-toggle="tooltip" data-placement="top"
                                    title="Restaurar Esta Base De Datos" id="${db.pk}" onclick="${restore}">
                                    <i class="fas fa-database"></i>
                                    Restaurar
                                </button>
                            </td>
                        </tr>
                    `)
                });
                return false;
            })
    })

    removeCard.addEventListener('click', (e) => {
        e.preventDefault()
        document.querySelector("#togle_table").setAttribute('hidden', 'hidden')
        empty(document.querySelector('#table_show_db'))
        restoreDB.removeAttribute('disabled')
    })
}
