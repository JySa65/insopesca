import axios from "../utils/axios";
import getCookie from "../utils/get_cookie";
import empty from "empty-element";
import yo from "yo-yo";
import swal from "sweetalert2";
import togglePassword from "../utils/toggle_password";

const checkEmail = data => {
  const config = {
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  };
  return axios.post("/forgot-password/", data, config);
};

const checkAnswers = data => {
  const config = {
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  };
  return axios.put("/forgot-password/", data, config);
};

const btn_recovery = document.querySelector("#recovery_password");
if (btn_recovery) {
  btn_recovery.onsubmit = e => {
    e.preventDefault();
    const email = document.querySelector("#id_email");
    const csrfmiddlewaretoken = document.getElementsByName(
      "csrfmiddlewaretoken"
    )[0];
    checkEmail({
      csrfmiddlewaretoken: csrfmiddlewaretoken.value,
      email: email.value
    })
      .then(data => {
        const error_message = document.querySelector("#alert_forgot");
        if (data.data.status) {
          error_message.innerHTML = "";
          const root = document.querySelector("#root_forgot");
          empty(root).append(
            template(data.data.data.questions, data.data.data.email)
          );
        } else {
          const html = `
        <div class="alert alert-danger" role="alert">
          ${data.data.msg}
        </div>
        `;
          error_message.innerHTML = html;
        }
      })
      .catch(err => console.log(err));
  };
}

const template = (questions, email) => yo`
  <div>
    <div class="form-group text-center">
      <label><b>Usuario: </b> <span id="id_email">${email}</span></label>
    </div>
    ${questions.map((question, i) => {
      return yo`
        <div class="form-group">
          <label for="${question.id}" class="col-form-label"><b>Pregunta:</b> ${
        question.question
      }</label>
          <input type="password"  class="form-control" autocomplete="off" required name="answer" id="${
            question.id
          }">
          <span toggle="#password-field" class="fa fa-fw fa-eye field-icon toggle-password" onclick="${togglePassword}"></span>
        </div>
      `;
    })}
    <button type="submit" onclick="${sendAnswers}" class="btn btn-primary btn-lg btn-block">Enviar Respuestas</button>
  </div>
    `;

const sendAnswers = e => {
  e.preventDefault();
  const email = document.querySelector("#id_email").textContent;
  const inputAnswers = document.getElementsByName("answer");
  const error_message = document.querySelector("#alert_forgot");

  if (
    inputAnswers[0].value == "" ||
    inputAnswers[1].value == "" ||
    inputAnswers[2].value == ""
  ) {
    const html = `
      <div class="alert alert-danger" role="alert">
        Algunos Campos Son Requeridos
      </div>
      `;
    error_message.innerHTML = html;
    return false;
  }

  const answers = [
    { id: inputAnswers[0].getAttribute("id"), answer: inputAnswers[0].value },
    { id: inputAnswers[1].getAttribute("id"), answer: inputAnswers[1].value },
    { id: inputAnswers[2].getAttribute("id"), answer: inputAnswers[2].value }
  ];
  const csrfmiddlewaretoken = document.getElementsByName(
    "csrfmiddlewaretoken"
  )[0];
  const data = {
    email,
    answers,
    csrfmiddlewaretoken: csrfmiddlewaretoken.value
  };
  checkAnswers(data).then(data => {
    if (data.data.status) {
      swal
        .fire({
          type: "success",
          title: "Exito",
          text: data.data.msg,
          showConfirmButton: true
        })
        .then(result => {
          if (result.value) {
            window.location.href = "/";
          }
        });
    } else {
      const html = `
          <div class="alert alert-danger" role="alert">
            ${data.data.msg}
          </div>
          `;
      error_message.innerHTML = html;
      return false;
    }
  });
};
