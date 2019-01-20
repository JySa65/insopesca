import swal from 'sweetalert2'

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
      confirmButtonText: 'Si'
    }).then((result) => {
      if (result.value) {
        swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success'
        )
      }
    })
  }
}

