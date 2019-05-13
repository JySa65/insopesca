import swal from 'sweetalert2';
import axios from 'axios';
import getCookie from '../../utils/get_cookie.js';
import validInput from '../../utils/validInput.js';
import deleteSwalCompany from '../../utils/delete_with_swal.js';

const id_repre_form = document.querySelector("#id_representative_form")
if (id_repre_form) {
    document.querySelector("#id_document").addEventListener(
        "keypress", (event) => validInput('n', 12, event))

    document.querySelector("#id_name").addEventListener(
        "keypress", (event) => validInput('l', 50, event))

    document.querySelector("#id_last_name").addEventListener(
        "keypress", (event) => validInput('l', 50, event))
    

    document.querySelector("#id_tlf").addEventListener(
        "keypress", (event) => validInput('n', 11, event))

    document.querySelector("#id_tlf_house").addEventListener(
        "keypress", (event) => validInput('n', 11, event))
    
}


const deleteReprcompany = (password, company) => {
    
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(company, { password }, config)
}

const btn_delete_repre_company = document.querySelector("#btn_delete_repre_company")
if (btn_delete_repre_company) {
    btn_delete_repre_company.addEventListener('click', (e) => {
        e.preventDefault()
        const url = btn_delete_repre_company.getAttribute("href")
        deleteSwalCompany(url, deleteReprcompany)
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
