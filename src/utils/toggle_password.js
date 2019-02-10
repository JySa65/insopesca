module.exports = (e) => {
  const input = e.path[1].children[1]
  const icon = e.path[0]
  if (input.getAttribute("type") == "password") {
    input.setAttribute("type", "text")
    icon.classList.remove("fa-eye")
    icon.classList.add("fa-eye-slash")
  } else {
    input.setAttribute("type", "password")
    icon.classList.remove("fa-eye-slash")
    icon.classList.add("fa-eye")
  }
}
