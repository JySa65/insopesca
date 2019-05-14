import swal from 'sweetalert2';
import axios from 'axios';
import getCookie from '../../utils/get_cookie.js';
import deleteSwalCompany from '../../utils/delete_with_swal.js';


const deletespecie = (password, company) => {
    
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(company, { password }, config)
}


const btn_delete_specie = document.querySelector("#btn_delete_specie")
if (btn_delete_specie) {
    btn_delete_specie.addEventListener('click', (e) => {
        e.preventDefault()
        const url = btn_delete_specie.getAttribute("href")
        deleteSwalCompany(url, deletespecie)
            .then((result) => {
                if (result.value) {
                    const data = result.value
                    swal.fire({
                        type: "success",
                        titleText: data.msg,
                        showConfirmButton: false,
                        timer: 1000
                    })
                    window.location.href = "http://localhost:8000/acuicultura/species/list/"
                }
            })
    })
}
