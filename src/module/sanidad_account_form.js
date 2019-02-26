const date = new Date().getFullYear();
const endDate = new Date(date - 18, 1,1)
const startDate = new Date(date - 100, 1,1)

$('#id_birthday').datepicker({
    language: 'es',
    title: "Insopesca",
    autoclose: true,
    endDate,
    startDate
});
