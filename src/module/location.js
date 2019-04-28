import axios from "../utils/axios";

const state = document.querySelector("#id_state");
const municipality = document.querySelector("#id_municipality");
const parish = document.querySelector("#id_parish");

if (state && municipality && parish) {
  state.onchange = e => {
    axios.get(`/api/municipality/${state.value}`).then(data => {
      const result = JSON.parse(data.data);
      let el = `<option value="" selected="">---------</option>`;
      result.map(data => {
        el += `<option value="${data.pk}">${data.fields.name}</option>`;
      });
      municipality.innerHTML = el;
    });
  };
}

if (municipality && parish) {
  municipality.onchange = e => {
    axios.get(`/api/parish/${municipality.value}`).then(data => {
      const result = JSON.parse(data.data);
      let el = `<option value="" selected="">---------</option>`;
      result.map(data => {
        el += `<option value="${data.pk}">${data.fields.name}</option>`;
      });
      parish.innerHTML = el;
    });
  };
}
