const rating = document.querySelector("form[name=reting]");

rating.addEventListener("click", function (e) {
  let data = new FormData(this);

  fetch(`${this.action}`, { method: "POST", body: data })
    // .then((response) => alert("Рейтинг установлен"))
    .catch((error) => (alert = "Ошибка"));

  rating.querySelector(".icon-favourites").classList.toggle("active");
});
// console.log(rating);
