let set_time = null;
input = document.querySelector(".search-header__input");
pop_up = document.querySelector(".search-header__extradition");

function StartEvent(obj) {
  if (obj) {
    obj.addEventListener("input", StartTimeout);
  }
}

function StartTimeout() {
  clearTimeout(set_time);
  set_time = setTimeout(SearchProduct, 1000);
}

function SearchProduct() {
  this_obj = document.querySelector(".search-header__input");
  if (this_obj.value.length >= 3) {
    RequestAjax(this_obj.value);
  }

  if (this_obj.value.length == 0) {
    pop_up.classList.remove("active");
    pop_up.innerHTML = "";
  }
}

function RequestAjax(e) {
  url = `/search-product-ajax/?search=${e}`;
  fetch(url, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      RenderProductSearch(data);
    })
    .catch((error) => console.log("Ошибка"));
}

function RenderProductSearch(data) {
  let html = "";
  pop_up.classList.add("active");

  if (data["product_list"].length == 0) {
    template = `
    <div class="search-header__item">
        <a class="search-header__link">Похоже что ничего не найдено.</a>
    </div>`;

    return (pop_up.innerHTML = template);
  }

  for (item of data["product_list"]) {
    template = `
    <div class="search-header__item">
        <a class="search-header__link" href="${item["url"]}">${item["name"]}</a>
    </div>`;

    html += template;
  }
  pop_up.innerHTML = html;
}

function values_search_form() {
  // Вставка поискового значения из get

  const search_input = document.querySelector(".search-header__input");
  if (search_input) {
    let _p = location.search.replace("?", "").split("&");
    _p.forEach((x) => {
      let args = x.split("=");
      if (args[0] == "qu") search_input.value = args[1];
    });
  }
}

values_search_form();
StartEvent(input);
