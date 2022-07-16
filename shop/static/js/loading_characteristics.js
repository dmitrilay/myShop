const btn_tabs = document.querySelectorAll(".tabs__btn[data-index*='1']");

if (btn_tabs) {
  btn_tabs[0].addEventListener("click", LoadingCharacteristics);
}

function LoadingCharacteristics() {
  const product_name = document.querySelector(".details-product__header");

  //   if (product_name) {
  //     console.log(product_name);
  //   }

  url = `/product-detail-spec-ajax/?product=${product_name.innerText}`;
  fetch(url, { method: "GET" })
    .then((response) => {
      //   console.log(response.json());
      return response.json();
    })
    .then((data) => {
      Render(data);
    })
    .catch((error) => (alert = "Ошибка"));
}

function Render(data) {
  console.log(data);
  for (item of data["spec"]) {
    p = `${html}`;
    console.log(html.indexOf('${item}'));
  }
}

html =
  '\
<div class="description-list__item">\
    <div class="description-list__item-title">${item}</div>\
    <div class="description-list__item-content"></div>\
</div>';

html2 = `    
<div class="description-list__item-row">
    <div class="description-list__item-name">${1}</div>
    <div class="description-list__item-value">196 г</div>
</div>`;
