import yo from 'yo-yo'
import empty from "empty-element";

const id_new_lagoon = document.querySelector('#id_new_lagoon')
const id_new_well = document.querySelector('#id_new_well')
if (id_new_lagoon && id_new_well) {
    const data = []
    const dataWell = [] 

    const onChange = (index, dat) => e => dat[index][e.target.name] = e.target.value

    const deleteRow = (index, status=true) => () => {
        if(status){
            data.splice(index, 1)
            return render('#id_data_lagoon', data, lagoon_template)
        }
        else {
            dataWell.splice(index, 1)
            render('#id_data_well', dataWell, well_template)
        }
    }

    const getSpecies = (index, number) => e => {
        const value = e.target.value
        const key = data[index]['sistem_cultive']['species']
        key[number] = value
    }

    const species_template = index => e => {
        const $root = document.querySelector(`#id_species_${index}`)
        data[index][e.target.name]['type'] = e.target.value
        data[index]['sistem_cultive']['species'] = []
        let number = 0
        switch (e.target.value) {
            case 'mono':
                number = 1
                break;
            case 'duo':
                number = 2
                break;
            default:
                break;
        }
        const emt = empty($root)
        for (let i = 0; i < number; i++) {
            emt.append(
                yo`
                    <div class="col-md-6 col-sm-12">
                        <label class="col-form-label">
                            Especies N° ${i + 1}
                        </label>
                        <select name="specie" class="form-control" onchange=${getSpecies(index, i)} required>
                            <option>-------------</option>
                            ${species.map(specie => yo`
                                <option value=${specie.id}>${specie.name}</option>
                            `)}
                        </select>
                    </div>               
                `
            ) 
        }
    }

    const lagoon_template = (id, index, value = "") => {
        return yo`
            <div class="row mb-4">
                <div class="col-sm-10">
                    <div class="row" id=${index}>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Diametro de la Laguna Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" name="diameter" id="${id}" value="${value.diameter}"
                                    onchange="${onChange(index, data)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Profundidad de la Laguna Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" name="deepth" id="${id}" value="${value.deepth}"
                                    onchange="${onChange(index, data)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <label for="${id}" class="col-form-label">
                                Sistema de Cultivo Nro° ${index +1}
                            </label>
                            <select name="sistem_cultive" required class="form-control" onchange="${species_template(index)}">
                                <option ${!value.sistem_cultive.type ? 'selected' : ''}>------------</option>
                                <option ${value.sistem_cultive.type == 'mono' ? 'selected' : ''}     value="mono">Mono Cultivo</option>
                                <option ${value.sistem_cultive.type == 'duo' ? 'selected' : ''}     value="duo">Duo Cultivo</option>
                            </select>
                        </div>
                        <div class="col-md-6 col-sm-12"></div>
                        <div class="col-sm-12 mt-4">
                            <div id="id_species_${index}" class="row">
                            ${value.sistem_cultive.species.length >= 1 
                                ? value.sistem_cultive.species.map((data, i) => {
                                    return yo`
                                        <div class="col-md-6 col-sm-12">
                                        <label class="col-form-label">
                                            Especies N° ${i + 1}
                                        </label>
                                        <select name="specie" class="form-control" onchange=${getSpecies(index, i)} required>
                                            <option>-------------</option>
                                            ${species.map(specie => {
                                                return data == specie.id
                                                ? yo`<option selected value=${specie.id}>${specie.name}</option>`
                                                    : yo`<option value=${specie.id}>${specie.name}</option>`
                                            })}
                                        </select>
                                    </div>    
                                    `
                                })
                                : ''
                            }
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-2">
                    <button type="button" class="btn btn-danger" style="margin: 30px 0 0 0;" data-toggle="tooltip" data-placement="top"
                        title="Eliminar Fila" onclick="${deleteRow(index)}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `
    }

    const well_template = (id, index, value="") => {
        return yo`
            <div class="row mb-4">
                <div class="col-sm-10">
                    <div class="row" id=${index}>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Diametro del Pozo Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" name="diameter" id="${id}" value="${value.diameter}"
                                    onchange="${onChange(index, dataWell)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Profundidad del Pozo Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" name="deepth" id="${id}" value="${value.deepth}"
                                    onchange="${onChange(index, dataWell)}" required autocomplete="off">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-2">
                    <button type="button" class="btn btn-danger" style="margin: 30px 0 0 0;" data-toggle="tooltip" data-placement="top"
                        title="Eliminar Fila" onclick="${deleteRow(index, false)}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `
    }

    const render = (id, dat, template) => {
        const $root = document.querySelector(id)
        const html = []
        const emt = empty($root)
        dat.forEach((item, index) => html.push(
            template("id_well", index, item)))
        html.forEach(inp => {
            emt.append(inp)
        })
    }

    
    id_new_lagoon.addEventListener('click', () => {
        data.push({
            diameter: "",
            deepth: "",
            sistem_cultive: {
                type: "",
                species: []
            },
        })
        return render('#id_data_lagoon', data, lagoon_template)
    })

    id_new_well.addEventListener('click', () => {
        dataWell.push({
            diameter: "",
            deepth: ""
        })
        render('#id_data_well', dataWell, well_template)
    })

}


// import swal from 'sweetalert2';
// import axios from 'axios';
// import getCookie from '../../utils/get_cookie.js';
// import validInput from '../../utils/validInput.js';
// import deleteSwalCompany from '../../utils/delete_with_swal.js';

// const new_wells = document.querySelector("#id_new_number_well");
// // const new_lagoon = document.querySelector("#id_new_number_lagoon");
// const multiwells = document.querySelector("#multinew_wells");
// // const multilagoon = document.querySelector("#multinew_lagoon");

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

// if (new_wells) {
//   const html = (name, number) => `
//     <h5>Pozo Nro° ${number}</h5>
//         <div class="row">
//             <div class="col-md-6 col-sm-12">
//                 <div class="form-group">
//                     <label for="new_well_diameter${number}" 
//                     class="col-form-label">Diametro del Pozo Nro° ${number}</label>
//                     <input class="form-control" name=new_wells_diameter_${name} id=new_wells_diameter_${number}>
//                 </div>
//             </div>
//             <div class="col-md-6 col-sm-12">
//                 <div class="form-group">
//                     <label for="new_well_deepth${number}" 
//                     class="col-form-label">Profundidad del Pozo Nro° ${number}</label>
//                     <input class="form-control" name=new_wells_deepth_${name} id=new_wells_deepth_${number}>
//                 </div>
//             </div>

//         </div>

//     `;

//   new_wells.onkeyup = e => {
//     const value = e.target.value;
//     let input = "";
//     cont = 0;
//     for (let i = 0; i < value; i++) {
//       cont = i + 1;
//       input += html(i, cont);
//     }
//     multiwells.innerHTML = input;
//   };
// }


// const id_tracing_form = document.querySelector("#id_representative_form")
// if (id_tracing_form) {
//     document.querySelector("#id_document_repre").addEventListener(
//         "keypress", (event) => validInput('n', 12, event))

//     document.querySelector("#id_name_repre").addEventListener(
//         "keypress", (event) => validInput('g', 50, event))

//     document.querySelector("#id_last_name_repre").addEventListener(
//         "keypress", (event) => validInput('g', 50, event))


//     document.querySelector("#id_phone_repre").addEventListener(
//         "keypress", (event) => validInput('n', 11, event))

//     document.querySelector("#id_landline_repre").addEventListener(
//         "keypress", (event) => validInput('n', 11, event))

// }


// const deletetracing = (password, company) => {

//     const config = {
//         headers: {
//             "X-CSRFToken": getCookie("csrftoken"),
//         }
//     }
//     return axios.post(company, { password }, config)
// }


// const btn_delete_tracing = document.querySelector("#btn_delete_tracing")
// if (btn_delete_tracing) {
//     btn_delete_tracing.addEventListener('click', (e) => {
//         e.preventDefault()
//         const url = btn_delete_tracing.getAttribute("href")
//         deleteSwalCompany(url, deletetracing)
//             .then((result) => {
//                 if (result.value) {
//                     const data = result.value
//                     swal.fire({
//                         type: "success",
//                         titleText: data.msg,
//                         showConfirmButton: false,
//                         timer: 1000
//                     })
//                     window.location.href = "http://localhost:8000/acuicultura/"
//                 }
//             })
//     })
// }
