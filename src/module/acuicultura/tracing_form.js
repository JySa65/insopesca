import yo from 'yo-yo'
import swal from 'sweetalert2';
import empty from "empty-element";
import axios from '../../utils/axios'
import getCookie from '../../utils/get_cookie.js';
import deleteSwalCompany from '../../utils/delete_with_swal.js';

const id_new_lagoon = document.querySelector('#id_new_lagoon')
const id_new_well = document.querySelector('#id_new_well')
const id_illegal_superfaces = document.querySelector('#id_illegal_superfaces')
const id_permise_superfaces = document.querySelector('#id_permise_superfaces')
const id_regular_superfaces = document.querySelector('#id_regular_superfaces')
const id_form_tracing = document.querySelector('#id_form_tracing')
const alert_message = document.querySelector('#alert_message')

if (id_new_lagoon && id_new_well) {
    const data = []
    const dataWell = []
    let dataSave = {
        lagoon: [],
        well: [],
        illegal_superfaces: 0,
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

    const species_template = (index, dat = { specie: "", number_specie: 0 }) => e => {
        const $root = document.querySelector(`#id_species_${index}`)
        data[index][e.target.name]['type'] = e.target.value

        let number = 0
        switch (e.target.value) {
            case 'mono':
                number = 1
                data[index].sistem_cultive.species = [{}]
                break;
            case 'poli':
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
                                    <input class="form-control" id="id_input_${index}${i}" type="number" step="any" name="number_specie" required autocomplete="off" readonly onchange=${getNumberSpecie(index, i)}>
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
                                    Ancho de la Laguna Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" step="any" name="diameter" id="${id}" value="${value.diameter}"
                                    onchange="${onChange(index, data)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Largo de la Laguna Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" step="any" name="deepth" id="${id}" value="${value.deepth}"
                                    onchange="${onChange(index, data)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Altura de la Laguna Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" step="any" name="height" id="${id}" value="${value.height}"
                                    onchange="${onChange(index, data)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <label for="${id}" class="col-form-label">
                                Sistema de Cultivo Nro° ${index + 1}
                            </label>
                            <select name="type" required class="form-control" onchange="${onChange(index, data)}">
                                <option ${!value.type ? 'selected' : ''} value="">------------</option>
                                <option ${value.type == 'circular' ? 'selected' : ''}     value="circular">Circular</option>
                                <option ${value.type == 'rectangular' ? 'selected' : ''}     value="rectangular">Rectangular</option>
                                <option ${value.type == 'irregular' ? 'selected' : ''}     value="irregular">Irregular</option>
                            </select>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <label for="${id}" class="col-form-label">
                                Sistema de Cultivo Nro° ${index + 1}
                            </label>
                            <select name="sistem_cultive" required class="form-control" onchange="${species_template(index)}">
                                <option ${!value.sistem_cultive.type ? 'selected' : ''} value="">------------</option>
                                <option ${value.sistem_cultive.type == 'mono' ? 'selected' : ''} value="mono">Mono Cultivo</option>
                                <option ${value.sistem_cultive.type == 'duo' ? 'selected' : ''} value="poli">Poli Cultivo</option>
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
                                                    <input class="form-control" id="id_input_${index}${i}" type="number" step="any" name="number_specie" required autocomplete="off" onchange=${getNumberSpecie(index, i)} value=${data.number_specie}>
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
                                <input class="form-control" type="number" step="any" name="diameter" id="${id}" value="${value.diameter}"
                                    onchange="${onChange(index, dataWell)}" required autocomplete="off">
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="form-group">
                                <label for="${id}" class="col-form-label">
                                    Profundidad del Pozo Nro° ${index + 1}
                                </label>
                                <input class="form-control" type="number" step="any" name="deepth" id="${id}" value="${value.deepth}"
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
            height: "",
            type: "",
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
    id_permise_superfaces.addEventListener('change', e => onChangeInput(e))
    id_regular_superfaces.addEventListener('change', e => onChangeInput(e))

    const saveData = data => {
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
        const btn_tracing_form = document.querySelector('#btn_tracing_form')
        btn_tracing_form.setAttribute('disabled', 'disabled')
        dataSave = {
            ...dataSave,
            lagoon: data,
            well: dataWell
        }

        return saveData(dataSave)
            .then(data => {
                const { status, msg } = data.data
                if (!status) {
                    window.scrollBy(0, -10000)
                    alert_message.removeAttribute('hidden')
                    alert_message.children[0].textContent = msg
                    btn_tracing_form.removeAttribute('disabled')
                } else {
                    window.location.href = `/acuicultura/production/unit/detail/${object_pk}/`
                }
            })
    })
}

const tracingDetailDelete = document.querySelector("#tracing_detail_delete")
if (tracingDetailDelete) {
    const deleteTracing = (password, company) => {
        const config = {
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        }
        return axios.post(company, { password }, config)
    }
    tracingDetailDelete.addEventListener('click', (e) => {
        e.preventDefault()
        const url = tracingDetailDelete.getAttribute("href")
        deleteSwalCompany(url, deleteTracing)
            .then((result) => {
                if (result.value) {
                    const data = result.value
                    swal.fire({
                        type: "success",
                        titleText: data.msg,
                        showConfirmButton: false,
                        timer: 1000
                    })
                    window.location.href = "http://localhost:8000/acuicultura/production/unit/List/"
                }
            })
    })
}
