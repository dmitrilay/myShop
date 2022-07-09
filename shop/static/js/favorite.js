document.addEventListener("DOMContentLoaded", ready);

const rating = document.querySelector("form[name=reting]");

if (rating) {
  rating.addEventListener("click", function (e) {
    let data = new FormData(this);

    fetch(`${this.action}`, { method: "POST", body: data })
      // .then((response) => alert("Рейтинг установлен"))
      .catch((error) => (alert = "Ошибка"));

    rating.querySelector(".icon-favourites").classList.toggle("active");
  });
}

function ready() {
  fetch("/account/favoritesBoolAjax", { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      PutFavorites(data);
    })
    .catch((error) => (alert = "Ошибка"));
}

function PutFavorites(data) {
  const listProduct = document.querySelectorAll("[data-id-product]");

  for (i of listProduct) {
    for (item of data["total"]) {
      if (i.dataset.idProduct == item["id_product"]) {
        i.classList.add("active");
      }
    }
  }
}
