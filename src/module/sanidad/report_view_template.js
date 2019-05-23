import yo from 'yo-yo'


const template = (data, index) => yo`
<div class="accrodion-regular">
    <div id="accordion3">
        <div class="card">
            <div class="card-header" id="heading_${index}">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}" aria-controls="collapse">
                        <span class="fas fa-angle-down mr-3"></span>
                        ${data.type_company.toUpperCase()}
                    </button >
                </h5 >
                <h5>Total De Inspección: ${data.inspections.length}</h5>
            </div >
    <div id="collapse${index}" class="collapse" aria-labelledby="heading_${index}" data-parent="#accordion3">
        <div class="card-body">
            <p class="lead"> ${data.company}</p>
            ${data.inspections.length == 0 
                ? yo`Hasta el Momento no tiene inspecciones`
                : data.inspections.map(inspection => {
                    return yo`
                    <div class="card">
                        <div class="border-top card-footer p-0 text-center">
                            <div class="campaign-metrics d-xl-inline-block">
                                <h4 class="mb-0">${inspection.fields.date}</h4>
                                <p>Fecha de Inspección</p>
                            </div>
                            <div class="campaign-metrics d-xl-inline-block">
                                <h4 class="mb-0">${inspection.fields.next_date}</h4>
                                <p>Proxima Inspección</p>
                            </div>
                        </div>
                        <div class="border-top card-footer p-0 text-center">
                            <div class="campaign-metrics d-xl-inline-block">
                                <h4 class="mb-0">
                                    ${inspection.fields.result == 'is_bad' 
                                    ? yo`
                                        <img src="/static/assets/images/bad.jpg" alt="" class="user-avatar-lg">
                                    `
                                    : inspection.fields.result == 'is_good'
                                    ? yo`
                                        <img src="/static/assets/images/good.jpg" alt="" class="user-avatar-lg">
                                    `
                                    : yo`
                                        <img src="/static/assets/images/verygood.jpg" alt="" class="user-avatar-lg">
                                    `
                                    }
                                </h4>
                                <p>Resultado</p>
                            </div>
                            <div class="campaign-metrics d-xl-inline-block">
                                    <h4 class="mb-0">${inspection.fields.notes}</h4>
                                    <p>Observación</p>
                            </div>
                        </div>
                    </div>
                    `
                })}
                </div>
            </div>
        </div>      
    </div >
</div >    
`
export default template
