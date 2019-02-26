import calculeDay from '../../utils/Date_periodic'

const date = $('#id_date')
const next_date = $('#id_next_date')
const result = $('#id_result')

date.datepicker({
    language: 'es',
    title: "Insopesca",
    autoclose: true,
}).on('hide', (e) => {
    if (e.target.value != "" && result.val() != "") {
        calculeDay(e.target.value, result.val(), next_date)
    }
});

next_date.datepicker({
    language: 'es',
    title: "Insopesca",
    autoclose: true,
});

$('#id_result').change((e) => {
    if (result.val() != "" && date.val() != "") {
        calculeDay(date.val(), result.val(), next_date)
    }
})


