setTimeout(FixSliderAddCart, 1000, (counter = 1));

function FixSliderAddCart(counter) {
  // Костыль для slider product, вешаются события на дупликаты слайдера
  const slider = document.querySelector(".product-slider__wrapper");
  let buttons_add_cart = "";

  if (slider) {
    buttons_add_cart = slider.querySelectorAll(".swiper-slide-duplicate");
  } else if (counter == 2) {
    return;
  } else {
    setTimeout(FixSliderAddCart, 2000, counter + 1);
  }

  for (i of buttons_add_cart) {
    btn_add = i.querySelector(".product-card__buttom");
    btn_add.addEventListener("click", addToCart);
  }
}

const buttons_add_cart = document.querySelectorAll(".product-card__buttom");
const form_cart = document.querySelector(".cart_add_js");
const button_add_cart = document.querySelector(".details-product__btn");

if (button_add_cart) {
  button_add_cart.addEventListener("click", addToCart);
}

for (let item of buttons_add_cart) {
  item.addEventListener("click", addToCart);
}

//-------------------------------
function animationFun(button_add_cart, product_item) {
  const product_image = product_item.querySelector(".product-card__img img");

  button_add_cart.classList.add("_fly");
  const cart = document.querySelector(".header__cart");
  const product_image_fly = product_image.cloneNode(true);
  const fly_width = product_image.offsetWidth;
  const fly_height = product_image.offsetHeight;
  const fly_top = product_image.getBoundingClientRect().top;
  const fly_left = product_image.getBoundingClientRect().left;

  product_image_fly.setAttribute("class", "_flyImage _ibg");
  product_image_fly.style.cssText = `
              left: ${fly_left}px;
              top: ${fly_top}px;
              width: ${fly_width}px;
              height: ${fly_height}px;
              opacity: 1;
              position: fixed;
              z-index: 100;
              transition: all 1s ease 0s;`;

  document.body.append(product_image_fly);

  // Координаты корзины
  const car_fly_left = cart.getBoundingClientRect().left;
  const car_fly_top = cart.getBoundingClientRect().top;

  product_image_fly.style.cssText = `
              left: ${car_fly_left}px;
              top: ${car_fly_top}px;
              width: 0px;
              height: 0px;
              opacity: 0;
              position: fixed;
              z-index: 100;
              transition: all 1s ease 0s;`;

  product_image_fly.addEventListener("transitionend", function () {
    if (button_add_cart.classList.contains("_fly")) {
      product_image_fly.remove();
      button_add_cart.classList.remove("_fly");
    }
  });
}

//-------------------------------
function addToCart(self) {
  self.preventDefault();
  let button_add_cart = self.target;
  const product_item = button_add_cart.closest(".product-card");

  if (!button_add_cart.classList.contains("_hold")) {
    button_add_cart.classList.add("_hold");
    if (product_item) {
      animationFun(button_add_cart, product_item);
    }

    // const form_buttom = button_add_cart.closest("form");
    // updateCart(form_buttom);
    addToCartFun(button_add_cart);
    setTimeout(() => button_add_cart.classList.remove("_hold"), 1500);
  }
}

//-------------------------------
function updateCart(form_buttom) {
  const data = new FormData(form_buttom);
  fetch(`${form_buttom.action}`, { method: "POST", body: data })
    // .then((response) => alert("Рейтинг установлен"))
    .catch((error) => (alert = "Ошибка"));
}

//-------------------------------
function addToCartFun(form_buttom) {
  fetch(`${form_buttom.href}`, { method: "GET" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      QuantityFun(data);
    })
    .catch((error) => (alert = "Ошибка"));
}

//-------------------------------
function QuantityFun(data) {
  const counter_cart = document.querySelector(".cart-header__counter");
  counter_cart.innerHTML = ` ${data["total"]} `;
  counter_cart.style.cssText = "";
}
