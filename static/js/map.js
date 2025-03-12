let map = L.map("map", {
  center: [55.983639506959385, 12.299427317600154],
  zoom: 13,
  scrollWheelZoom: false,
});
let marker = L.marker([55.983639506959385, 12.299427317600154]).addTo(map);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);
