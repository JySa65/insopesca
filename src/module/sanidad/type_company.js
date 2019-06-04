import swal from 'sweetalert2'
import getCookie from '../../utils/get_cookie'
import axios from '../../utils/axios'
import deleteSwal from '../../utils/delete_with_swal'
 
const config = {
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
    }
}
const updateTypeCompany = (data) => axios.put('/sanidad/type_company/', data, config)


const deleteTypeCompany = (data) => axios.post(`/sanidad/type_company/`, data, config)

const getSwalGeneral = (id, func, info) => swal.fire({
        type: 'info',
        title: info.title,
        input: info.input,
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        preConfirm: (value) => {
            const data = { value, id }
            return func(data)
                .then(response => {
                    if (!response.data.status) {
                        throw new Error(response.data.msg)
                    }
                    return new Promise((resolve, reject) => {
                        console.log(resolve.data)
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
    })



const getUpdateView = (id) => getSwalGeneral(id, updateTypeCompany, 
    { title: "Ingrese El Nuevo Tipo De compañia", input: "text"})
    .then(value => {
        if (value.value) {
            swal.fire({
                type: 'success',
                titleText: 'Tipo De Compañia Actualizada',
            }).then(() => window.location.reload())
        }
    })

const getDeleteView = (id) => getSwalGeneral(id, deleteTypeCompany,
    { title: "Ingreser Su Contraseña", input: "password" })
    .then(value => {
        if (value.value) {
            swal.fire({
                type: 'success',
                titleText: value.value.msg,
            }).then(() => window.location.reload())
        }
    })

const $id_type_company_list = document.querySelector("#id_type_company_list")
if ($id_type_company_list) {
    $id_type_company_list.addEventListener('click', e => {
        let name = e.target.name
        if (name == 'update' || name == 'delete'){
            const id = e.srcElement.parentElement.parentElement.id
            switch (name) {
                case 'update':
                    getUpdateView(id)
                    break;
                case 'delete':
                    getDeleteView(id)
                    break;
                default:
                    break;
            }
        }
    })
}
