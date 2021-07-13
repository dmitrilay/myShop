$(function() {
  // Owl Carousel
  var owl = $(".owl-carousel");
  owl.owlCarousel({
    items: 4,
    margin: 0,
    loop: true,
    nav: false,
    touchDrag: true,
    mouseDrag: true,
    autoplay: true,
    smartSpeed: 200,
    dots: false,
    responsive:{0:{items:2,},600:{items:3,},1000:{items:4,}}
  });
});

