import swal from 'sweetalert2'

export default (id, func) => {
    return swal.fire({
        type: 'info',
        title: "Ingrese Su Clave",
        input: 'password',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        preConfirm: (data) => {
            return func(data, id)
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
    })

}
