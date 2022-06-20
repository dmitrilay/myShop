// =======================================================
// Slider-product
// =======================================================
const thumbsSwiper = new Swiper("#swiper-thumbs", {
  slidesPerView: 4,
  watchSlidesProgress: true,
  freeMode: true,
  spaceBetween: 2,
});

const slider_product = new Swiper("#swiper-product", {
  slidesPerView: 1,
  loop: true,
  thumbs: {
    swiper: thumbsSwiper
  },
});



