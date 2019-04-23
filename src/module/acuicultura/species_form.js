import validInput from '../../utils/validInput.js';
const id_species_form = document.querySelector("#id_species_form")
if (id_species_form) {
    document.querySelector("#id_ordinary_name").addEventListener(
        "keypress", (event) => validInput('l', 50, event))

    document.querySelector("#id_scientific_name").addEventListener(
        "keypress", (event) => validInput('l', 50, event))
    
}
