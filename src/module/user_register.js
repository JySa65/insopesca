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