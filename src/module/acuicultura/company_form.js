import swal from 'sweetalert2';
import axios from 'axios';
import getCookie from '../../utils/get_cookie.js';
import validInput from '../../utils/validInput.js';
import deleteSwalCompany from '../../utils/delete_with_swal.js';

const id_form_company_acui = document.querySelector("#id_form_company_acuicultura")
if (id_form_company_acui) {
    document.querySelector("#id_name").addEventListener(
        "keypress", (event) => validInput('g', 50, event))

    document.querySelector("#id_tlf").addEventListener(
        "keypress", (event) => validInput('n', 11, event))

    document.querySelector("#id_tlf_house").addEventListener(
        "keypress", (event) => validInput('n', 11, event))

    const $id_illegal_superfaces = document.querySelector("#id_illegal_superfaces")
    const $id_permise_superfaces = document.querySelector("#id_permise_superfaces")
    const $id_regular_superfaces = document.querySelector("#id_regular_superfaces")
    
    const enabledDisabled = (status, ids) => {
        if (status) {
            ids.forEach(id => {
                id.checked = false
                id.setAttribute("disabled", "disabled")
            })
        } else {
            ids.forEach(id => {
                id.checked = false
                id.removeAttribute('disabled')
            })
        }
    }

    $id_illegal_superfaces.addEventListener('change', 
        e => enabledDisabled(e.target.checked, 
            [$id_permise_superfaces,$id_regular_superfaces]))
    
    $id_permise_superfaces.addEventListener('change', 
        e => enabledDisabled(e.target.checked, 
            [$id_illegal_superfaces]))

    $id_regular_superfaces.addEventListener('change', 
        e => enabledDisabled(e.target.checked, 
            [$id_illegal_superfaces]))
}

const deleteuni = (password, company) => {
    
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(company, { password }, config)
}


const btn_delete_unit = document.querySelector("#btn_delete_unit")
if (btn_delete_unit) {
    btn_delete_unit.addEventListener('click', (e) => {
        e.preventDefault()
        const url = btn_delete_unit.getAttribute("href")
        deleteSwalCompany(url, deleteuni)
            .then((result) => {
                if (result.value) {
                    const data = result.value
                    swal.fire({
                        type: "success",
                        titleText: data.msg,
                        showConfirmButton: false,
                        timer: 1000
                    })
                    window.location.href = "/acuicultura/production/unit/List/"
                }
            })
    })
}
const btn_add_north = document.querySelector("#btn_add_north")
const btn_add_south = document.querySelector("#btn_add_south")
const btn_add_west = document.querySelector("#btn_add_west")
const btn_add_oest = document.querySelector("#btn_add_oest")

if (btn_add_north && btn_add_south && btn_add_west && btn_add_oest){
    btn_add_north.addEventListener('click', (e) => addLinderCompany(e, '#id_north'))
    btn_add_south.addEventListener('click', (e) => addLinderCompany(e, '#id_south'))
    btn_add_west.addEventListener('click', (e) => addLinderCompany(e, '#id_west'))
    btn_add_oest.addEventListener('click', (e) => addLinderCompany(e, '#id_oest'))
}
const saveData = (data) => {
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post('/acuicultura/linder/', { data }, config)
}

const addLinderCompany = (e, id) => {
    e.preventDefault()
    const input = document.querySelector(id)
    swal.fire({
        type: 'info',
        title: "Ingrese La Localización",
        text: "Recuerde Que No Se Podra Eliminar Luego",
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
            const idSelects = ['#id_north', '#id_south', '#id_west', '#id_oest']
            const data = result.value
            idSelects.forEach(idSelect => {
                const select = document.querySelector(idSelect)
                select.innerHTML += `
                    <option value="${data.data.id}" ${id == idSelect ? 'selected': ''}>${data.data.name.replace(/\b[a-z]/g, c => c.toUpperCase())}</option>
                `
            });
            swal.fire({
                type: "success",
                titleText: data.msg,
                showConfirmButton: false,
                timer: 1000
            })
        }
    })
}
