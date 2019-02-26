const calculeDay = (date, result, input) => {
    const [day, month, year] = date.split('/')
    const dateTo = new Date(year, month - 1, day)
    let newDate = ""
    switch (result) {
        case 'is_verygood':
            newDate = new Date(dateTo.getFullYear(),
                dateTo.getMonth() + 6, dateTo.getDate())
            break;
        case 'is_good':
            newDate = new Date(dateTo.getFullYear(),
                dateTo.getMonth() + 3, dateTo.getDate())
            break;
        case 'is_bad':
            newDate = new Date(dateTo.getFullYear(),
                dateTo.getMonth() + 1, dateTo.getDate())
            break;
        default:
            newDate = new Date(dateTo.getFullYear(),
                dateTo.getMonth() + 1, dateTo.getDate());
            break;
    }
    const day_fer = newDate.getDay()
    if (day_fer == 0) {
        newDate = new Date(newDate.getFullYear(), newDate.getMonth(), newDate.getDate() + 1)
    }
    if (day_fer == 6) {
        newDate = new Date(newDate.getFullYear(), newDate.getMonth(), newDate.getDate() + 2)
    }
    input.datepicker('update', newDate);
}

export default calculeDay
