import swal from 'sweetalert2'
import axios from '../utils/axios'

const is_super = document.querySelector("#id_is_superuser")
if (is_super) {
	is_super.onclick = e => {
		const role_level = document.querySelector("#role_level")
		const value = e.target.checked
		if (value) {
			role_level.setAttribute("hidden", "hidden")
		} else {
			role_level.removeAttribute("hidden")
		}
	}
}

const role = document.querySelector("#id_role")
if (role) {
	role.onchange = e => {
		const role = document.querySelector("#role")
		const value = e.target.value
		const level = document.querySelector("#id_level")
		if (value == "is_coordinator") {
			role.setAttribute("hidden", "hidden")
			level.removeAttribute("required")
		} else {
			role.removeAttribute("hidden")
			level.setAttribute("required", "required")
			level.value = ""
		}
	}
}

const email = document.querySelector("#id_email")
const ci = document.querySelector("#id_ci")

if (email && email.getAttribute('data_type') == 'user' ||
	ci && ci.getAttribute('data_type')) {
	email.addEventListener('blur', () => searchUser(email.value))
	ci.addEventListener('blur', () => searchUser(ci.value))
}
const searchUser = (value) => {
	if (value != ''){
		axios.get(`/authentication/api/detail?data=${value}`)
			.then(data => {
				const {status, user } = data.data
				if (!status) return false
				
				if (user.is_delete) {
					return swal.fire({
						type: 'warning',
						titleText: `Usuario ${user.name} Esta Ihnabilitado del sistema ¿Desea Habilitarlo?`,
						showConfirmButton: true,
						showCancelButton: true
					}).then(status => {
						if (status.value) window.location.href = `/authentication/update/${user.pk}/?type=delete` 
					} )
				}
				
				if (!user.is_active) {
					return swal.fire({
						type: 'warning',
						titleText: `Usuario ${user.name} Existe pero esta inactivo ¿Desea Activarlo?`,
						showConfirmButton: true,
						showCancelButton: true
					}).then(status => {
						if (status.value) window.location.href = `/authentication/update/${user.pk}/?type=active`
					})
				}
				return swal.fire({
					type: 'warning',
					titleText: `Usuario ${user.name} Esta Registrado en el sistema ¿Desea Ver la Información?`,
					showConfirmButton: true,
					showCancelButton: true
				}).then(status => {
					if (status.value) window.location.href = `/authentication/detail/${user.pk}/`
				})
			})
	}
}
