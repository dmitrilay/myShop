// =======================================================
// Main-Slider
// =======================================================
const main_product = new Swiper(".slider-main", {
  slidesPerView: 1,
  slidesPerView: "auto",
  loop: true,
  spaceBetween: 10,

  breakpoints: {
    '@0.75': {
      spaceBetween: 10,
    },
    '@1.00': {
      spaceBetween: 20,
    },
    '@1.50': {
      spaceBetween: 30,
    },
  },
});
// =======================================================
// Main-Slider
// =======================================================
const slider_product = new Swiper("#product__slider", {
  // slidesPerView: "auto",
  slidesPerView: 4,
  loop: true,
  // spaceBetween: 30,
  autoHeight: false,

  breakpoints: {
    1: {
      slidesPerView: 2,
      spaceBetween: 10,
    },
    500: {
      slidesPerView: 3,
      spaceBetween: 15,
    },
    800: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
    1100: {
      slidesPerView: 5,
      spaceBetween: 25,
    },
  },
  // centeredSlides: true,

  // pagination: {
  //   el: ".swiper-pagination",
  //   clickable: true,
  // },

});

// =======================================================
// Slider-DEMO
// =======================================================
// const thumbsSwiper = new Swiper("#swiper-thumbs", {
//   slidesPerView: 4,
//   loop: true,
//   spaceBetween: 32,

//   breakpoints: {
//     '@0.75': {
//       spaceBetween: 0,
//     },
//     '@1.00': {
//       spaceBetween: 20,
//     },
//     '@1.50': {
//       spaceBetween: 30,
//     },
//   },

//   thumbs: {
//     swiper: thumbsSwiper
//   },
// });

