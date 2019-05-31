import yo from 'yo-yo'

const template = (inspection) => yo`
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <label class="h4 text-primary">Inspeciones Vencidas</label>
            </div>
            <div class="card-body">
                ${inspection.map((data, index) => yo`
                <div class="mt-3">
                    <table class="table table-bordered">
                        <thead>
                            <tr class="table-dark">
                                <th class="">#</th>
                                <th class="">Tipo</th>
                                <th class="">Nombre</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td>${index + 1}</td>
                            <td>${data.type_company.toUpperCase()}</td>
                            <td>${data.name.toUpperCase()}</td>
                        </tbody>
                    </table>
                    <table class="table table-bordered">
                        <thead>
                            <tr class="table-dark">
                                <th>Ultima Inspección</th>
                                <th>Fecha De Vencimiento</th>
                                <th>Usuario Responsable</th>
                                <th>Observaciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <th>${data.inspection.date}</th>
                            <th>${data.inspection.pass_date}</th>
                            <th>
                                ${data.inspection.result == 'is_bad'
                                ? yo`
                                <img src="/static/assets/images/bad.jpg" alt="" class="user-avatar-lg" title="Malo"
                                    data-toggle="tooltip" data-placement="top">
                                `
                                : data.inspection.result == 'is_good'
                                ? yo`
                                <img src="/static/assets/images/good.jpg" alt="" class="user-avatar-lg" title="Bueno"
                                    data-toggle="tooltip" data-placement="top">
                                `
                                : yo`
                                <img src="/static/assets/images/verygood.jpg" alt="" class="user-avatar-lg"
                                    title="Muy Bueno" data-toggle="tooltip" data-placement="top">
                                `
                                }
                            </th>
                            <th>${data.inspection.notes}</th>
                        </tbody>
                    </table>
                </div>
                `)}
                <div class="row mt-5">
                    <div class="col-12 text-center">
                        <a href="/reports/sanidad/inspection/" class="btn btn-lg btn-success" target="_blank">
                            <i class="far fa-file-pdf"></i>
                            Generar PDF
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
`
export default template
