const _p = document.querySelectorAll(".item-input__add-input a");
const button_save = document.querySelectorAll("#button_save");

if (_p) {
  _p[0].addEventListener("click", add_input);
}

if (button_save) {
  button_save[0].addEventListener("click", to_save_data);
}

function add_input(e) {
  const wrapper_input = document.querySelector(".item-input");
  const item = document.querySelectorAll(".item-input__wraper");
  const simpleCopy = item[0].cloneNode(true);

  _s = wrapper_input.appendChild(simpleCopy);
  _s = _s.querySelectorAll("input");
  _s.forEach((_i) => (_i.value = ""));
}

function to_save_data(e) {
  const item = document.querySelectorAll(".item-input__wraper");
  const product_id = document.querySelector(".form-select");

  let list = {};
  for (let _i of item) {
    _v = _i.querySelector('[name="spec"]').value;
    _v2 = _i.querySelector('[name="value"]').value;
    if (_v) list[_v] = _v2;
  }

  if (product_id.value) {
    obj = {};
    obj["product_id"] = product_id.value;
    obj["spec"] = list;
    product_id.value != "---" ? RequestAjax(obj) : console.log("Не выбран продукт");
  }
}

function RequestAjax(list) {
  //   console.log(list);
  //   const token = document.querySelector("#csrf_token input");
  //   csrfToken = token.value;

  csrf = document.cookie;
  csrf = getCookie("csrftoken");
  //   console.log(csrf);
  //   console.log(csrfToken);

  const headers = new Headers({
    "Content-Type": "x-www-form-urlencoded",
    "X-CSRFToken": csrf,
  });

  json = JSON.stringify(list);
  url = `/spec/create-characteristic/`;
  fetch(url, { method: "POST", headers: headers, body: json })
    .then((response) => {
      return response.json();
    })
    .catch((error) => console.log("Ошибка"));
}

function getCookie(name) {
  let matches = document.cookie.match(
    new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") + "=([^;]*)")
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
