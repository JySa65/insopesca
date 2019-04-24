import swal from 'sweetalert2';
import axios from 'axios';
import getCookie from '../../utils/get_cookie.js';
import validInput from '../../utils/validInput.js';
import deleteSwalCompany from '../../utils/delete_with_swal.js';

const new_wells = document.querySelector("#id_new_number_well");
// const new_lagoon = document.querySelector("#id_new_number_lagoon");
const multiwells = document.querySelector("#multinew_wells");
// const multilagoon = document.querySelector("#multinew_lagoon");

// if (new_lagoon){
//     const html = (name, number) => `
//             <div id="multinew_lagoon">
//                 Diametro de la Laguna Nro°`+number+`
//             <input class="form-control" name=new_lagoon_diameter_${name} id=new_lagoon_diameter_${number}>

//             Profundidad de la Laguna Nro°`+number+`
//             <input class="form-control" name=new_lagoon_deepth_${name} id=new_lagoon_deepth_${number}>
//             <div>`
//             new_lagoon.onkeyup = (e) => {
//                 const value = e.target.value
//                 let input = ""
//                 cont = 0
//                 for (let i = 0; i < value; i++) {
//                     cont = i+1
//                     input += html(i,cont)
//                 }
//                 multilagoon.innerHTML = input

//             }

//     }

if (new_wells) {
  const html = (name, number) => `
    <h5>Pozo Nro° ${number}</h5>
        <div class="row">
            <div class="col-md-6 col-sm-12">
                <div class="form-group">
                    <label for="new_well_diameter${number}" 
                    class="col-form-label">Diametro del Pozo Nro° ${number}</label>
                    <input class="form-control" name=new_wells_diameter_${name} id=new_wells_diameter_${number}>
                </div>
            </div>
            <div class="col-md-6 col-sm-12">
                <div class="form-group">
                    <label for="new_well_deepth${number}" 
                    class="col-form-label">Profundidad del Pozo Nro° ${number}</label>
                    <input class="form-control" name=new_wells_deepth_${name} id=new_wells_deepth_${number}>
                </div>
            </div>

        </div>

    `;

  new_wells.onkeyup = e => {
    const value = e.target.value;
    let input = "";
    cont = 0;
    for (let i = 0; i < value; i++) {
      cont = i + 1;
      input += html(i, cont);
    }
    multiwells.innerHTML = input;
  };
}


const id_tracing_form = document.querySelector("#id_representative_form")
if (id_tracing_form) {
    document.querySelector("#id_document_repre").addEventListener(
        "keypress", (event) => validInput('n', 12, event))

    document.querySelector("#id_name_repre").addEventListener(
        "keypress", (event) => validInput('g', 50, event))

    document.querySelector("#id_last_name_repre").addEventListener(
        "keypress", (event) => validInput('g', 50, event))
    

    document.querySelector("#id_phone_repre").addEventListener(
        "keypress", (event) => validInput('n', 11, event))

    document.querySelector("#id_landline_repre").addEventListener(
        "keypress", (event) => validInput('n', 11, event))
    
}


const deletetracing = (password, company) => {
    
    const config = {
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    }
    return axios.post(company, { password }, config)
}


const btn_delete_tracing = document.querySelector("#btn_delete_tracing")
if (btn_delete_tracing) {
    btn_delete_tracing.addEventListener('click', (e) => {
        e.preventDefault()
        const url = btn_delete_tracing.getAttribute("href")
        deleteSwalCompany(url, deletetracing)
            .then((result) => {
                if (result.value) {
                    const data = result.value
                    swal.fire({
                        type: "success",
                        titleText: data.msg,
                        showConfirmButton: false,
                        timer: 1000
                    })
                    window.location.href = "http://localhost:8000/acuicultura/"
                }
            })
    })
}
