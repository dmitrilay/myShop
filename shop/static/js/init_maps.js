let location_maps = [54.924935, 73.454755];
let location_placemark = [54.924935, 73.454755];



function init() {
  let map = new ymaps.Map("map-test", {
    center: location_maps,
    zoom: 16,
  });
  let placemark = new ymaps.Placemark(location_placemark, {}, {});
  map.geoObjects.add(placemark);
}

ymaps.ready(init);
