const new_wells = document.querySelector("#id_new_number_well")
const new_lagoon = document.querySelector("#id_new_number_lagoon")
const multiwells = document.querySelector("#multinew_wells")
const multilagoon = document.querySelector("#multinew_lagoon")

if (new_lagoon){
    const html = (name, number) => `
            <div id="multinew_lagoon">
                Diametro de la Laguna Nro°`+number+`
            <input class="form-control" name=new_lagoon_diameter_${name} id=new_lagoon_diameter_${number}>

            Profundidad de la Laguna Nro°`+number+`
            <input class="form-control" name=new_lagoon_deepth_${name} id=new_lagoon_deepth_${number}>
            <div>`
            new_lagoon.onkeyup = (e) => {
                const value = e.target.value
                let input = ""
                cont = 0
                for (let i = 0; i < value; i++) {
                    cont = i+1
                    input += html(i,cont)
                }
                multilagoon.innerHTML = input
                    
            }


    }


if (new_wells){
    const html = (name, number) => `
            <div id="multinew_wells">
                Diametro del Pozo Nro°`+number+`
            <input class="form-control" name=new_wells_diameter_${name} id=new_wells_diameter_${number}>

            Profundidad del Pozo Nro°`+number+`
            <input class="form-control" name=new_wells_deepth_${name} id=new_wells_deepth_${number}>


            <div>`

    new_wells.onkeyup = (e) => {
        const value = e.target.value
        let input = ""
        cont = 0
        for (let i = 0; i < value; i++) {
            cont = i+1
            input += html(i,cont)
        }
        multiwells.innerHTML = input
    }
} 