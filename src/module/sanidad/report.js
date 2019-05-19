const report_select = document.querySelector("#id_report_select")
const date_1 = document.querySelector("#date_1")
const date_2 = document.querySelector("#date_2")
const form_date = document.querySelector("#date-form")
const specific_form = document.querySelector("#especific-form")


if (report_select) {
	report_select.onchange = e => {
		const value = e.target.value
		console.log(value)
		if (value == "is_for_date_company" || value == "is_for_date_driver" || value == "is_for_date_inpection") {
			form_date.removeAttribute("hidden")
			specific_form.setAttribute("hidden", "hidden")

		} else if (value == "is_especific_company" || value == "is_especific_driver" || value == "is_especific_inpection"){
			console.log("is_especific_company")
			form_date.setAttribute("hidden", "hidden")
			specific_form.removeAttribute("hidden")
			date_1.value = ""
			date_2.value = ""
        } else if (value == "is_all_company" || value == "is_all_driver" || value == "is_all_inpection"){
			form_date.setAttribute("hidden", "hidden")
			specific_form.setAttribute("hidden", "hidden")
			date_1.value = ""
			date_2.value = ""

		} 
	}
}

