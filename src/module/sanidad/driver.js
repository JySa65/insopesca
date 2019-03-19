import axios from 'axios'
import swal from 'sweetalert2';
import deleteSwalUser from '../../utils/delete_with_swal.js'
import getCookie from '../../utils/get_cookie.js'

const saveData = (password, ...args) => {
    const [driver] = args
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(`/sanidad/driver/delete/${driver}/`, { password }, config)
}

const btn_toggle_driver = document.querySelector("#btn_toggle_driver")
if (btn_toggle_driver) {
    btn_toggle_driver.addEventListener('click', (e) => {
        e.preventDefault()
        const id = btn_toggle_driver.getAttribute("data")
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
