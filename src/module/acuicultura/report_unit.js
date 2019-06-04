const $id_report_unit = document.querySelector("#id_report_unit")

if ($id_report_unit) {
    const $type = document.querySelector("#id_type")
    const $document = document.querySelector("#id_document")
    const $date_range1 = document.querySelector("#id_date_range1")
    const $date_range2 = document.querySelector("#id_date_range2")

    $type.addEventListener('change', e => {
        const value = $type.value
        $date_range1.value = ""
        $date_range2.value = ""
        $document.value = ""
        if (value == "all_unit") {
            $date_range1.removeAttribute("disabled")
            $date_range2.removeAttribute("disabled")
            $document.setAttribute("disabled", "disabled")
        } else {
            $document.removeAttribute("disabled")
            $date_range1.setAttribute("disabled", "disabled")
            $date_range2.setAttribute("disabled", "disabled")
        }
    })

    const date = new Date().getFullYear();
    const endDate = new Date(date + 1, 1, 1)
    const startDate = new Date(date - 100, 1, 1)

    $('#id_date_range1').datepicker({
        language: 'es',
        title: "Insopesca",
        autoclose: true,
        endDate,
        startDate,
        calendarWeeks: true,
        weekStart: 1,
        clearBtn: true
    });
    $('#id_date_range1').on('changeDate', e => {
        $('#id_date_range2').datepicker({
            language: 'es',
            title: "Insopesca",
            autoclose: true,
            endDate,
            calendarWeeks: true,
            weekStart: 1,
            clearBtn: true
        })
        $('#id_date_range2').datepicker('setStartDate', e.date)
    });

    $id_report_unit.addEventListener('submit', e => {
        e.preventDefault()
        const id_valid = document.querySelector('#id_valid')
        id_valid.value = 0
        if ($date_range1.value != '') {
            id_valid.value = 1
        }
        $id_report_unit.submit()
    })

}
