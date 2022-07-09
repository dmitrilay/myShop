const quantity = () => {
  const obj_quantity = document.querySelectorAll("[data-quantity]");
  for (obj_q of obj_quantity) {
    btn_all = obj_q.querySelectorAll("[data-q");
    for (let btn of btn_all) {
      btn.addEventListener("click", { handleEvent: action, obj_q: obj_q });
    }
  }

  function action(e) {
    const _target = e.currentTarget;
    const obj = this.obj_q.querySelector("input");
    let value = parseInt(obj.value);
    let id_product = e.target.closest("[data-quantity]").dataset.quantity;
    let form_quantity = e.target.closest("[data-quantity]");

    if (!form_quantity.classList.contains("_hold")) {
      form_quantity.classList.add("_hold");

      if (_target.dataset.q == "+") {
        AjaxAddItem("add", id_product);
        value += 1;
      } else if (_target.dataset.q == "-") {
        if (value > 1) {
          AjaxAddItem("reduce", id_product);
          value -= 1;
        }
      }
      obj.value = value;

      setTimeout(() => form_quantity.classList.remove("_hold"), 1000);
    }
  }
};

function AjaxAddItem(obj, id_product) {
  const url = `changeItemAjax/?item=${obj}&product_id=${id_product}`;
  //   console.log(url);
  fetch(url, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      WritePrice(data, id_product);
    })
    .catch((error) => (alert = "Ошибка"));
}

function WritePrice(data, id_product) {
  const obj_quantity = document.querySelectorAll("[data-quantity]");
  for (item of obj_quantity) {
    _p = item.dataset.quantity;
    if (_p == id_product) {
      _r = item.closest(".products-cart__price");
      if (_r) {
        _price = _r.querySelector(".products-cart__total-price span");
        _price.innerHTML = data["total_price_item"];
      }
    }
  }
  const total_price = document.querySelector(".total-cost-cart__price span");
  total_price.innerHTML = data["total_price"];
  document.querySelector(".cart-header__counter").innerHTML = data["cart_item"];
}

quantity();
