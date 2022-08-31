const btn_tabs = document.querySelectorAll(".tabs__btn[data-index*='1']");

if (btn_tabs) {
  btn_tabs[0].addEventListener("click", LoadingCharacteristics, { once: true });
}

function LoadingCharacteristics() {
  const product_name = document.querySelector(".details-product__header");

  if (!product_name) {
    return;
  }

  args = encodeURIComponent(product_name.innerText);
  url = `/product-detail-spec-ajax/?product=${args}`;

  fetch(url, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      Render(data);
    })
    .catch((error) => console.log("Ошибка"));
}

function Render(data) {
  // Построение страницы
  if (data["spec"].length == 0) return;

  let list_sub_cat = [];
  for (item of data["spec"]) {
    list_sub_cat.push(item["name_spec__subcategory__name"]);
  }

  const unique_sub = Array.from(new Set(list_sub_cat));

  p = "";
  for (item of unique_sub) {
    p += item_html;
    values_html = "";

    for (value_item of data["spec"]) {
      _p = html2;
      if (item == value_item["name_spec__subcategory__name"]) {
        _p = _p.replace("{{key}}", value_item["name_spec__name"]);
        _p = _p.replace("{{value}}", value_item["name_value__name"]);
        values_html += _p;
      }
    }
    p = p.replace("{{key}}", item);
    p = p.replace("{{value}}", values_html);
  }

  const spec_write = document.querySelector(".description-list");
  spec_write.innerHTML = p;
}

item_html = `
<div class="description-list__item">
    <div class="description-list__item-title">{{key}}</div>
    <div class="description-list__item-content">{{value}}</div>
</div>`;

html2 = `    
<div class="description-list__item-row">
    <div class="description-list__item-name">{{key}}</div>
    <div class="description-list__item-value">{{value}}</div>
</div>`;
