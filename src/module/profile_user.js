import swal from 'sweetalert2'
import axios from '../utils/axios'
import getCookie from '../utils/get_cookie'

const restoreData = (pk) => {
  const config = {
    headers :{
      "X-CSRFToken": getCookie("csrftoken"),
    }
  }
  return axios.post('authentication/restore-data/', {pk}, config)
}

const restore_data = document.querySelector("#restore_data");
if (restore_data) {
  restore_data.onclick = e => {
    swal.fire({
      title: '¿Esta Seguro?',
      text: "¡De Restablecer los datos!",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si',
      preConfirm: () => {
        restoreData(restore_data.getAttribute("data"))
        .then(data => true)
        .catch(err => false)
      }
    }).then((result) => {
      if (result.value) {
        swal.fire(
          'Exito!',
          'Usuario Restablecido',
          'success'
        )
        setTimeout(() => {
          window.location.reload()
        }, 1000)
      }
    })
  }
}

