import yo from 'yo-yo'

const template = (data, index) => yo`
<div class="accrodion-regular mt-2">
    <div id="accordion3">
        <div class="card" style="background: #c3daf3;">
            <div class="card-header" id="heading_${index}">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapse${index}"
                        aria-expanded="false" aria-controls="collapse${index}" aria-controls="collapse">
                        <span class="fas fa-angle-down mr-3"></span>
                        ${data.type_company.toUpperCase()}
                        <p>
                            <b>Total de inspecciones:</b> ${data.inspection_total}
                        </p>
                    </button>
                </h5>
            </div>
            <div id="collapse${index}" class="collapse" aria-labelledby="heading_${index}" data-parent="#accordion3">
                <div class="card-body">
                    ${data.companys.map(company => {
                    return yo`
                    <div class="card mt-2">
                        <div class="card-header">
                            <p class="lead">${company.name.toUpperCase()}</p>
                        </div>
                        <div class="card-body p-3">
                            <div class="table-responsive">
                                <table class="table table-hover table-bordered">
                                    <thead class="bg-light">
                                        <tr>
                                            <th>#</th>
                                            <th>Fecha de Inspección</th>
                                            <th>Proxima Inspección</th>
                                            <th>Resultado</th>
                                            <th>Observación</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${company.inspections.length == 0
                                        ? yo`Hasta el Momento no tiene inspecciones`
                                        : company.inspections.map((inspection, i) => {
                                        return yo`
                                        <tr>
                                            <td>${i+1}</td>
                                            <td>${inspection.fields.date}</td>
                                            <td>${inspection.fields.next_date}</td>
                                            <td>
                                                ${inspection.fields.result == 'is_bad'
                                                ? yo`
                                                <img src="/static/assets/images/bad.jpg" alt="" class="user-avatar-lg" title="Malo" data-toggle="tooltip" data-placement="top">
                                                `
                                                : inspection.fields.result == 'is_good'
                                                ? yo`
                                                <img src="/static/assets/images/good.jpg" alt="" class="user-avatar-lg" title="Bueno" data-toggle="tooltip" data-placement="top" >
                                                `
                                                : yo`
                                                <img src="/static/assets/images/verygood.jpg" alt="" class="user-avatar-lg" title="Muy Bueno" data-toggle="tooltip" data-placement="top">
                                                `
                                                }
                                            </td>
                                            <td>${inspection.fields.notes}</td>
                                        </tr>
                                        `
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    `
                    })}
                </div>
            </div>
        </div>
    </div>
</div>
`
export default template
