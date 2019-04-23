import validInput from '../../utils/validInput.js';
const id_form_company_acui = document.querySelector("#id_form_company_acuicultura")
if (id_form_company_acui) {
    document.querySelector("#id_document").addEventListener(
        "keypress", (event) => validInput('n', 12, event))

    document.querySelector("#id_name").addEventListener(
        "keypress", (event) => validInput('g', 50, event))

    document.querySelector("#id_tlf").addEventListener(
        "keypress", (event) => validInput('n', 11, event))

    document.querySelector("#id_tlf_house").addEventListener(
        "keypress", (event) => validInput('n', 11, event))
    
}
