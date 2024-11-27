// Initialize the map
const map = L.map('map').setView([50.0647, 19.9450], 12); // Center the map on Kraków with a suitable zoom level

// Add the tile layer (map tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Updated reservoir data with coordinates in Kraków
const reservoirs = [
    {
        id: 1,
        name: "Bagry",
        coordinates: [50.0346, 19.9844],
        air_temperature: 12,
        water_temperature: 18,
        pressure: 1013,
        noise_level: 15
    },
    {
        id: 2,
        name: "Zalew Nowohucki",
        coordinates: [50.0731, 20.0411],
        air_temperature: 24,
        water_temperature: 10,
        pressure: 1015,
        noise_level: 45
    },
    {
        id: 3,
        name: "Zakrzówek",
        coordinates: [50.0396, 19.9229],
        air_temperature: 20,
        water_temperature: 17,
        pressure: 1012,
        noise_level: 58
    },
    {
        id: 4,
        name: "Przylasek Rusiecki",
        coordinates: [50.0655, 20.1318],
        air_temperature: 5,
        water_temperature: 35,
        pressure: 1014,
        noise_level: 62
    },
    {
        id: 5,
        name: "Kryspinów",
        coordinates: [50.0467, 19.7793],
        air_temperature: -15,
        water_temperature: 21,
        pressure: 1011,
        noise_level: 100
    }
];

// Function to update gauges with selected reservoir data
function updateGauges(reservoir) {
    updateGauge('airTempGauge', reservoir.air_temperature);
    updateGauge('waterTempGauge', reservoir.water_temperature);
    updateGauge('pressureGauge', reservoir.pressure);
    updateGauge('noiseLevelGauge', reservoir.noise_level);
}

// Function to select a reservoir by ID (triggered from sidebar)
function selectReservoir(reservoirId) {
    const reservoir = reservoirs.find(res => res.id === reservoirId);
    if (reservoir) {
        updateGauges(reservoir);
    } else {
        console.error('Reservoir not found!');
    }
}

// Add markers to the map for each reservoir
reservoirs.forEach(reservoir => {
    const marker = L.marker(reservoir.coordinates)
        .addTo(map)
        .bindPopup(`<b>${reservoir.name}</b>`);

    // On marker click, update gauges with the reservoir's data
    marker.on('click', () => {
        updateGauges(reservoir);
    });
});
