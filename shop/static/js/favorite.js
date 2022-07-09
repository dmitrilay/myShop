document.addEventListener("DOMContentLoaded", ready);

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

// Добавить товар в избранное
const click_favorite = document.querySelectorAll(".icon-favourites[data-id-product]");

if (click_favorite) {
  for (item of click_favorite) {
    item.addEventListener("click", ClickFavorite);
  }
}

function ClickFavorite(e) {
  const favourites = e.target;

  if (!favourites.classList.contains("_hold")) {
    favourites.classList.add("_hold");
    url = `/account/favoritesAddAjax/?idProduct=${favourites.dataset.idProduct}`;
    fetch(url, { method: "GET" })
      // .then((response) => alert("Рейтинг установлен"))
      .catch((error) => (alert = "Ошибка"));
    favourites.classList.toggle("active");

    setTimeout(() => favourites.classList.remove("_hold"), 1000);
  }
}
