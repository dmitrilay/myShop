// =======================================================
// Slider-product2
// =======================================================
const thumbsSwiper = new Swiper("#swiper-thumbs", {
  slidesPerView: 4,
  watchSlidesProgress: true,
  freeMode: true,
  spaceBetween: 2,
});

const slider_product2 = new Swiper("#swiper-product", {
  slidesPerView: 1,
  loop: true,
  thumbs: {
    swiper: thumbsSwiper
  },
});



