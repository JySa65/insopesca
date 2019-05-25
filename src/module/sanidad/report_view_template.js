import yo from 'yo-yo'


const template = (data, index) => yo`
<div class="accrodion-regular">
    <div id="accordion3">
        <div class="card" style="background: #c3daf3;">
            <div class="card-header" id="heading_${index}">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapse${index}"
                        aria-expanded="false" aria-controls="collapse${index}" aria-controls="collapse">
                        <span class="fas fa-angle-down mr-3"></span>
                        ${data.type_company.toUpperCase()}
                    </button>
                </h5>
            </div>
            <div id="collapse${index}" class="collapse" aria-labelledby="heading_${index}" data-parent="#accordion3">
                <div class="card-body">
                    ${data.companys.map(company => {
                        return yo`
                            <div class="card mt-2">
                                <div class="card-header">
                                    <p class="lead">${company.name}</p>
                                </div>
                                <div class="card-body">
                                    
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
