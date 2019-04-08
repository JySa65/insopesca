import validInput from "../../utils/validInput.js";

const transportForm = document.querySelector("#form_transport");

if (transportForm) {
  // land
  const registration = document.querySelector("#id_registration");
  const model = document.querySelector("#id_model");
  const brand = document.querySelector("#id_brand");
  const load_capacity = document.querySelector("#id_load_capacity");

  // fluvial
  const name_fluvial = document.querySelector("#id_name_fluvial");
  const result = document.querySelector("#id_result");

  // maritime
  const name = document.querySelector("#id_name");
  const year_vessel = document.querySelector("#id_year_vessel");

  if (registration && model && brand && load_capacity) {
    registration.addEventListener("keypress", event =>
      validInput("g", 7, event)
    );
    model.addEventListener("keypress", event => validInput("g", 50, event));
    brand.addEventListener("keypress", event => validInput("g", 50, event));
    load_capacity.addEventListener("keypress", event =>
      validInput("n", 8, event)
    );
  }

  if (name_fluvial && result) {
    name_fluvial.addEventListener("keypress", event => validInput("g", 20, event));
    result.addEventListener("keypress", event => validInput("g", 9999, event));
  }

  if (name && year_vessel) {
    name.addEventListener("keypress", event => validInput("g", 20, event));
    year_vessel.addEventListener("keypress", event => validInput("n", 4, event));
  }
}
