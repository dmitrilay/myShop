let location_p1 = [55.02503016881296, 73.37193227909847];
let location_p2 = [55.024899, 73.370359];

function init() {
  let map = new ymaps.Map("map-test", {
    center: location_p1,
    zoom: 16,
  });
  let placemark = new ymaps.Placemark(location_p2, {}, {});
  map.geoObjects.add(placemark);
}

ymaps.ready(init);
