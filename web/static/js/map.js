// Function to update gauges with selected reservoir data
function updateGauges(reservoir) {
    updateGauge('airTempGauge', reservoir.air_temperature);
    updateGauge('waterTempGauge', reservoir.water_temperature);
    updateGauge('pressureGauge', reservoir.pressure);
    updateGauge('noiseLevelGauge', reservoir.noise_level);
}

function selectReservoir(reservoirId, reservoirs) {
    const reservoir = reservoirs.find(res => res.id === reservoirId);
    if (reservoir) {
        updateGauges(reservoir);
    }
}

function addReservoirMarkers(reservoirs, map) {
    reservoirs.forEach(reservoir => {
        const marker = L.marker(reservoir.coordinates)
            .addTo(map)
            .bindPopup(`<b>${reservoir.name}</b>`);

        marker.on('click', () => {
            updateGauges(reservoir);
        });
    });
}

function bindReservoirSelection(reservoirs) {
    const submenu = document.getElementById('reservoirsSubmenu');
    submenu.addEventListener('click', event => {
        if (event.target.tagName === 'A') {
            event.preventDefault();
            const reservoirId = parseInt(event.target.getAttribute('data-reservoir-id'), 10);
            selectReservoir(reservoirId, reservoirs);
        }
    });
}

