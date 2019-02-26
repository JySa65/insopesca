const onlyNumber = (e) => {
    let key = (document.all) ? e.keyCode : e.which;
    //Tecla de retroceso para borrar, siempre la permite
    if (key == 8) return true;
    // Patron de entrada, en este caso solo acepta numeros
    const pattern = /[0-9]/;
    let finalKey = String.fromCharCode(key);
    return pattern.test(finalKey);
}

const onlyLetter = (e) => {
    let key = (document.all) ? e.keyCode : e.which;
    //Tecla de retroceso para borrar, siempre la permite
    if (key == 8) return true;
    // Patron de entrada, en este caso solo acepta letras
    const pattern = /[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]/;
    let finalKey = String.fromCharCode(key);
    return pattern.test(finalKey);
}

const generalInput = (e) => {
    let key = (document.all) ? e.keyCode : e.which;
    //Tecla de retroceso para borrar, siempre la permite
    if (key == 8) return true;
    // Patron de entrada, en este caso solo los 2
    const pattern = /[A-Za-z0-9ÑñÁáÉéÍíÓóÚúÜü¿?.;\s]/;
    let finalKey = String.fromCharCode(key);
    return pattern.test(finalKey);
}

const removeSpace = (e) => {
    let txt = e.target.value.trim(), aux;
    do {
        aux = txt;
        txt = txt.replace("  ", " ");
    } while (txt !== aux);
        e.srcElement.value = txt;
}

const finalValid = (type_valid, max=null, event) => {
    if (type_valid == "l") {
        if (!onlyLetter(event)) event.preventDefault()
    }
    if (type_valid == "n") {
        if (!onlyNumber(event)) event.preventDefault()
    }
    if (type_valid == "g") {
        if (!generalInput(event)) event.preventDefault()
    }
    if (event.target.value.length >= max){
        event.preventDefault()
    }
    // event.target.onpaste = (event) => {
    //     event.preventDefault();
    // }
    event.target.onblur = (event) => {
        removeSpace(event);
    }
}

export default finalValid;
