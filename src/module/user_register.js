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