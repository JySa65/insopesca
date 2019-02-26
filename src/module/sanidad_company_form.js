import swal from 'sweetalert2';
import axios from 'axios';
import getCookie from '../utils/get_cookie.js';
import validInput from '../utils/validInput.js';

const saveData = (data) => {
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post('/sanidad/type-company/', { data }, config)
}

const btn_add_type_company = document.querySelector('#btn_add_type_company')
if (btn_add_type_company) {
    btn_add_type_company.onclick = (e) => {
        swal.fire({
            type: 'info',
            title: "Ingrese el Tipo De Compañia",
            input: 'text',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Añadir',
            cancelButtonText: 'Cancelar',
            showLoaderOnConfirm: true,
            preConfirm: (data) => {
                return saveData(data)
                    .then(response => {
                        if (!response.data.status) {
                            throw new Error(response.data.msg)
                        }
                        return new Promise((resolve, reject) => {
                            resolve(response.data)
                        })
                    })
                    .catch(error => {
                        swal.showValidationMessage(
                            `${error}`
                        )
                    })
            },
            allowOutsideClick: false
        }).then((result) => {
            if (result.value) {
                const data = result.value
                document.querySelector("#id_type_company").innerHTML += `
                    <option value="${data.data.id}" selected="">${data.data.name.replace(/\b[a-z]/g, c => c.toUpperCase())}</option>
                `
                swal.fire({
                    type: "success",
                    titleText: data.msg,
                    showConfirmButton: false,
                    timer: 1000
                })
            }
        })
    }
}

const id_form_company = document.querySelector("#id_form_company")
if (id_form_company) {
    document.querySelector("#id_document").addEventListener(
        "keypress", (event) => validInput('n', 12, event))

    document.querySelector("#id_speg").addEventListener(
        "keypress", (event) => validInput('n', 4, event))

    document.querySelector("#id_name").addEventListener(
        "keypress", (event) => validInput('g', 50, event))

    document.querySelector("#id_tlf").addEventListener(
        "keypress", (event) => validInput('n', 11, event))
}
