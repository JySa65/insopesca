import moment from 'moment'
const form_report_ugly = document.querySelector("#id_form_report_uglys")

if (form_report_ugly) {
    const selects = document.getElementById("id_type");
    const documents = document.getElementById("id_document");
    const date_1 = document.querySelector("#id_date_range1")
    const date_2 = document.querySelector("#id_date_range2")
    const new_date_1 = document.querySelector("#id_date_range1_text")
    const new_date_2 = document.querySelector("#id_date_range2_text")

    selects.onchange = e => {
        const val = e.target.value
        if (val == "all_company" || val == "all_driver"){
            documents.disabled = true;
            date_1.disabled = false;
            date_2.disabled = false;
            date_1.value = "";
            date_2.value = "";
            new_date_1.value = "";
            new_date_2.value = "";
        
        } else if (val == ""){
            documents.disabled = true;
            date_1.disabled = true;
            date_2.disabled = true;
            date_1.value = "";
            date_2.value = "";
            new_date_1.value = "";
            new_date_2.value = "";

        } else if (val == "individual_company" || val == "individual_driver" ) {
            documents.disabled = false;
            date_1.disabled = true;
            date_2.disabled = true;
            date_1.value = "";
            date_2.value = "";
            new_date_1.value = "";
            new_date_2.value = "";

        } else{
            date_1.value = "";
            date_2.value = "";
            new_date_1.value = "";
            new_date_2.value = "";
            documents.disabled = true;
            date_1.disabled = true;
            date_2.disabled = true;

        }
    }
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
        const year = moment(e.date).format('YYYY');
        const week = moment(e.date).format('WW');
        const value = `${year}-${week}`
        document.querySelector(`#id_date_range1_text`).value = value
        document.querySelector('#id_date_range2').value = ''
        document.querySelector(`#id_date_range2_text`).value = ''
        changeDate2(e.date)
    });

    const changeDate2 = date => {
        $('#id_date_range2').datepicker({
            language: 'es',
            title: "Insopesca",
            autoclose: true,
            endDate,
            calendarWeeks: true,
            weekStart: 1,
            clearBtn: true
        }).on('changeDate', e => {
            const year = moment(e.date).format('YYYY');
            const week = moment(e.date).format('WW');
            const value = `${year}-${week}`
            document.querySelector(`#id_date_range2_text`).value = value
        });
        $('#id_date_range2').datepicker('setStartDate', date)
    } 
}

// if (form_report_ugly){
//     const selects = document.getElementById("id_type");
//     const document = document.getElementById("id_document");
    // const date_1 = document.getElementById("date_range1")
    // const date_2 = document.getElementById("date_range2")
    // selects.onchange = e => {
    //     const val = e.target.value

    //     if (val == "" || val == "all_company " || val == "all_driver"){
    //         console.log(":D:D:")
            
    //     }
    // }

    // const date = new Date().getFullYear();
    // const endDate = new Date(date + 1, 1, 1)
    // const startDate = new Date(date - 100, 1, 1)

    // $('#id_date_range1').datepicker({
    //     language: 'es',
    //     title: "Insopesca",
    //     autoclose: true,
    //     endDate,
    //     startDate,
    //     calendarWeeks: true,
    //     weekStart: 1,
    //     clearBtn: true
    // });
    // $('#id_date_range1').on('changeDate', e => {
    //     const year = moment(e.date).format('YYYY');
    //     const week = moment(e.date).format('WW');
    //     const value = `${year}-${week}`
    //     document.querySelector(`#id_date_range1_text`).value = value
    //     document.querySelector('#id_date_range2').value = ''
    //     document.querySelector(`#id_date_range2_text`).value = ''
    //     changeDate2(e.date)
    // });

    // const changeDate2 = date => {
    //     $('#id_date_range2').datepicker({
    //         language: 'es',
    //         title: "Insopesca",
    //         autoclose: true,
    //         endDate,
    //         calendarWeeks: true,
    //         weekStart: 1,
    //         clearBtn: true
    //     }).on('changeDate', e => {
    //         const year = moment(e.date).format('YYYY');
    //         const week = moment(e.date).format('WW');
    //         const value = `${year}-${week}`
    //         document.querySelector(`#id_date_range2_text`).value = value
    //     });
    //     $('#id_date_range2').datepicker('setStartDate', date)
    // }
// }
