import yo from 'yo-yo'
import empty from "empty-element";
import axios from '../../utils/axios'
import getCookie from '../../utils/get_cookie.js';

const id_new_lagoon = document.querySelector('#id_new_lagoon')
const id_new_well = document.querySelector('#id_new_well')
const id_illegal_superfaces = document.querySelector('#id_illegal_superfaces')
const id_irregular_superfaces = document.querySelector('#id_irregular_superfaces')
const id_permise_superfaces = document.querySelector('#id_permise_superfaces')
const id_regular_superfaces = document.querySelector('#id_regular_superfaces')
const id_form_tracing = document.querySelector('#id_form_tracing')

if (id_new_lagoon && id_new_well) {
    const data = []
    const dataWell = []
    let dataSave = {
        lagoon: [],
        well: [],
        illegal_superfaces: 0,
        irregular_superfaces: 0,
        permise_superfaces: 0,
        regular_superfaces: 0,
        well_current: well_current,
        laggon_current: laggon_current
    }

    const onChange = (index, dat) => e => dat[index][e.target.name] = e.target.value

    const onChangeInput = e => dataSave[e.target.name] = e.target.value

    const deleteRow = (index, status = true) => () => {
        if (status) {
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
        const id_input = document.querySelector(`#id_input_${index}${number}`)
        data[index].sistem_cultive.species[number]['specie'] = value
        data[index].sistem_cultive.species[number]['number_specie'] = 0
        id_input.value = ""
        id_input.removeAttribute('readonly')
        if (value == '') id_input.setAttribute('readonly', 'readonly')
    }

    const getNumberSpecie = (index, number) => e => {
        const value = e.target.value
        data[index].sistem_cultive.species[number]['number_specie'] = value
    }

    const species_template = (index, dat = { specie: "", number_specie:0 }) => e => {
        const $root = document.querySelector(`#id_species_${index}`)
        data[index][e.target.name]['type'] = e.target.value
        
        let number = 0
        switch (e.target.value) {
            case 'mono':
                number = 1
                data[index].sistem_cultive.species = [{}]
                break;
            case 'duo':
                number = 2
                data[index].sistem_cultive.species = [{}, {}]
                break;
            default:
                break;
        }
        const emt = empty($root)
        for (let i = 0; i < number; i++) {
            emt.append(
                yo`
                    <div class="col-sm-12">
                        <div class="row">
                            <div class="col-md-6 col-sm-12">
                                <label class="col-form-label">
                                    Especies N° ${i + 1}
                                </label>
                                <select name="specie" class="form-control" onchange=${getSpecies(index, i)} required>
                                    <option value="">-------------</option>
                                    ${species.map(specie => {
                                        return dat.specie == specie.id
                                            ? yo`<option selected value=${specie.id}>${specie.name}</option>`
                                            : yo`<option value=${specie.id}>${specie.name}</option>`
                                    })}
                                </select>
                            </div>               
                            <div class="col-md-6 col-sm-12">
                                <div class="form-group">
                                    <label class="col-form-label">
                                        Cantidad De Especie N° ${i + 1}
                                    </label>
                                    <input class="form-control" id="id_input_${index}${i}" type="number" name="number_specie" required autocomplete="off" readonly onchange=${getNumberSpecie(index,i)}>
                                </div>
                            </div>      
                        </div>
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
                                Sistema de Cultivo Nro° ${index + 1}
                            </label>
                            <select name="sistem_cultive" required class="form-control" onchange="${species_template(index)}">
                                <option ${!value.sistem_cultive.type ? 'selected' : ''} value="">------------</option>
                                <option ${value.sistem_cultive.type == 'mono' ? 'selected' : ''}     value="mono">Mono Cultivo</option>
                                <option ${value.sistem_cultive.type == 'duo' ? 'selected' : ''}     value="duo">Duo Cultivo</option>
                            </select>
                        </div>
                        <div class="col-md-6 col-sm-12"></div>
                        <div class="col-sm-12 mt-4">
                            <div id="id_species_${index}" class="row">
                            ${Object.keys(value.sistem_cultive.species[0]).length !== 0
                            ? value.sistem_cultive.species.map((data, i) => {
                                return yo`
                                    <div class="col-sm-12">
                                        <div class="row">
                                            <div class="col-md-6 col-sm-12">
                                                <label class="col-form-label">
                                                    Especies N° ${i + 1}
                                                </label>
                                                <select name="specie" class="form-control" onchange=${getSpecies(index, i)} required>
                                                    <option value="">-------------</option>
                                                    ${species.map(specie => {
                                                    return data.specie == specie.id
                                                        ? yo`<option selected value=${specie.id}>${specie.name}</option>`
                                                        : yo`<option value=${specie.id}>${specie.name}</option>`
                                                })}
                                                </select>
                                            </div>               
                                            <div class="col-md-6 col-sm-12">
                                                <div class="form-group">
                                                    <label class="col-form-label">
                                                        Cantidad De Especie N° ${i + 1}
                                                    </label>
                                                    <input class="form-control" id="id_input_${index}${i}" type="number" name="number_specie" required autocomplete="off" onchange=${getNumberSpecie(index, i)} value=${data.number_specie}>
                                                </div>
                                            </div>      
                                        </div>
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

    const well_template = (id, index, value = "") => {
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
                species: [{}]
            },
        })
        return render('#id_data_lagoon', data, lagoon_template)
    })

    id_new_well.addEventListener('click', () => {
        dataWell.push({
            diameter: "",
            deepth: ""
        })
        return render('#id_data_well', dataWell, well_template)
    })

    id_illegal_superfaces.addEventListener('change', e => onChangeInput(e))
    id_irregular_superfaces.addEventListener('change', e => onChangeInput(e))
    id_permise_superfaces.addEventListener('change', e => onChangeInput(e))
    id_regular_superfaces.addEventListener('change', e => onChangeInput(e))

    const saveData = data => {
        console.log(data)
        const pk = object_pk
        const url = `/acuicultura/tracing/add/${pk}`
        const config = {
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        }
        return axios.post(url, data, config);
    }

    id_form_tracing.addEventListener('submit', e => {
        e.preventDefault();
        dataSave = {
            ...dataSave,
            lagoon: data,
            well: dataWell
        }
        console.log(dataSave)
        window.scrollBy(0, -1000)
        return saveData(dataSave)
            .then(data => {
                console.log(data)
            })
    })
}
