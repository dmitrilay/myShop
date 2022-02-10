//запуск скрипта

$(".slider-for").slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  fade: true,
  asNavFor: ".slider",
});
$(".slider").slick({
  infinite: false,
  slidesToShow: 3,
  slidesToScroll: 1,
  asNavFor: ".slider-for",
  dots: false,
  centerMode: false,
  focusOnSelect: true,
  arrows: false,
});
