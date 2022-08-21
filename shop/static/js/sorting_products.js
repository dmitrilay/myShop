// document.addEventListener("DomContentLoaded", sorting_products);
document.addEventListener("DOMContentLoaded", sorting_products);

function sorting_products() {
  _select = document.querySelector(".product-menu-sort__select select");
  _filters = document.querySelector(".list-product__filters .filters");
  let _input_sort = "";
  let _get_array = [];

  if (_filters) {
    // Создаем input в форме filter, для записи данных sort_price
    let div = document.createElement("div");
    let input = document.createElement("input");
    div.style = "display: none;";
    input.name = "sort";
    input.value = "price_d";
    div.append(input);
    _filters.append(div);
    _input_sort = input;
  }

  if (location.search) {
    // разбор get запроса
    _get = decodeURIComponent(location.search);
    _get = _get.replace(/[+]/g, " ");
    _get_array = _get.substr(1).split("&");
  }

  if (_get_array) {
    for (_i of _get_array) {
      arg = _i.split("=");
      if (arg[0] == "sort") {
        _select.value = arg[1];
        _input_sort.value = arg[1];
      }
    }
  }

  _select.addEventListener("change", () => {
    if (_filters) {
      _input_sort.value = _select.value;
      let _btn = document.querySelector(".buttons-filters__btn");
      _btn.click();
    }
  });
}

// sort=price_low
// sort=price_high
// location.href = 'https://www.wildberries.ru'
// location.replace("https://www.wildberries.ru");

//   _sort = `sort=${_select.value}`;
//   _get = `${_get}&${_sort}`;
//   _url = `${location.host}${location.pathname}${_get}`;
//   //   print(location.host, location.pathname, location.search);
//   //   location.replace("https://www.wildberries.ru");
// } else {
//   _sort = `sort=${_select.value}`;
//   _sort = encodeURI(_sort);
//   _url = `${location.host}${location.pathname}&${_sort}`;
//   location.replace(`?${_sort}`);
// }
