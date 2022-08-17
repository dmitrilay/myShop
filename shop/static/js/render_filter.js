// render фильтра для продуктов
print = console.log;
//   ("use strict");
document.addEventListener("DOMContentLoaded", render_filter);

function render_filter(self, data) {
  if (data == undefined) {
    request_filter();
  }

  if (data != undefined) {
    parent_filter = document.querySelector(".filters__inner");
    html_item = document.querySelector(".filters__item ");
    add_html(parent_filter, html_item, data);
    add_in_input();
    start_accordion();
    sliderUI();
    parent_filter.style = "";
  }
}

function add_html(parent_filter, html_item, data) {
  function slider_price(item) {
    // Создание слайдера
    slider = document.querySelector(".item-filters.sl");
    elem = slider.cloneNode(true);
    elem.style = "";
    _input = elem.querySelectorAll(".item-filters__input input");
    _value = item["price_min_max"][0].split("-");
    _input[0].value = _value[0];
    _input[1].value = _value[1];
    slider.remove();
    parent_filter.append(elem);
  }

  _id = 1000;
  for (item of data) {
    if (item["price_min_max"]) {
      slider_price(item);
      continue;
    }

    elem = html_item.cloneNode(true);
    elem.querySelector(".item-filters__text").textContent = Object.keys(item);
    elem.style = "";

    wrapper_value = elem.querySelector(".item-filters__accordion");

    for (value_item of item[Object.keys(item)]) {
      _value = elem.querySelector(".item-filters__checkbox").cloneNode(true);
      _value.querySelector(".item-filters__checkbox-label").textContent = value_item;

      _value.querySelector(".custom-checkbox__input").name = Object.keys(item);
      _value.querySelector(".custom-checkbox__input").id = _id;
      _value.querySelector(".custom-checkbox__input").value = value_item;

      _value.querySelector(".custom-checkbox__label").setAttribute("for", _id);

      wrapper_value.append(_value);
      _id++;
    }
    elem.querySelectorAll(".item-filters__checkbox")[0].remove();
    parent_filter.append(elem);
  }
}

function request_filter() {
  url = `/filter-ajax/?cat=${location.pathname}`;
  fetch(url, { method: "GET" })
    .then((response) => response.json())
    .then((data) => request_processing(data));
  // .catch((error) => console.error("Ошибка"));
}

function request_processing(data) {
  priority = [];
  mySity = {};
  for (item of data["status"]) {
    if (mySity[item[0]]) {
      if (mySity[item[0]].indexOf(item[1]) == -1) {
        mySity[item[0]].push(item[1]);
      }
    } else {
      mySity[item[0]] = [item[1]];
      priority.push({ [item[0]]: item[2] });
    }
  }

  priority.sort((a, b) => (_r = Object.values(a) - Object.values(b)));
  for (item of priority) {
    item[Object.keys(item)] = mySity[Object.keys(item)];
  }
  return render_filter("none", priority);
}

function add_in_input() {
  url = location.search;
  url = decodeURI(url.substr(1));
  url = url.replace(/[+]/g, " ");
  m_url = url.split("&");

  let result = {};
  m_url.forEach((element) => {
    item = element.split("=");
    result[item[0]] ? result[item[0]].push(item[1]) : (result[item[0]] = [item[1]]);
  });

  item_filter = document.querySelector(".filters__inner");

  for (item in result) {
    if (item == "priceMin") {
      document.querySelector(`input[name='${item}']`).dataset["start"] = result[item];
      continue;
    } else if (item == "priceMax") {
      document.querySelector(`input[name='${item}']`).dataset["end"] = result[item];
      continue;
    }

    all_checkbox = item_filter.querySelector(`input[name="${item}"]`);
    if (all_checkbox) {
      all_checkbox = all_checkbox.closest(".item-filters");

      _y = all_checkbox.querySelector(".item-filters__title");
      if (_y) {
        _y.classList.add("_active");
        result[item].forEach((element) => {
          all_checkbox.querySelector(`input[value="${element}"]`).checked = true;
        });
      }
    }
  }
}
