import axios from 'axios'
import swal from 'sweetalert2';
import deleteSwalUser from '../../utils/delete_with_swal.js'
import getCookie from '../../utils/get_cookie.js'

const date = new Date().getFullYear();
const endDate = new Date(date - 18, 1,1)
const startDate = new Date(date - 100, 1,1)

$('#id_birthday').datepicker({
    language: 'es',
    title: "Insopesca",
    autoclose: true,
    endDate,
    startDate
});

const saveData = (password, ...args) => {
    const [company, account] = args[0]
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(`/sanidad/company/detail/${company}/account/delete/${account}/`, { password }, config)
}

const btn_toggle_account = document.querySelector("#btn_toggle_account")
if (btn_toggle_account) {
    btn_toggle_account.addEventListener('click', (e) => {
        e.preventDefault()
        const id = btn_toggle_account.getAttribute("data").split(",")
        deleteSwalUser(id, saveData)
            .then((result) => {
                if (result.value) {
                    const data = result.value
                    swal.fire({
                        type: "success",
                        titleText: data.msg,
                        showConfirmButton: false,
                        timer: 1000
                    })
                    window.location.reload()
                }
            })
    })
}
