function getHighestAirTemp(reservoirs) {
    var maxAirTemp = 0;
    var location;
    reservoirs.forEach(element => {
        console.log(element.air_temperature);
        if (element.air_temperature > maxAirTemp) {
            maxAirTemp = element.air_temperature
            location = element.name;
        }
    });
    var element = document.getElementById("highest-air-temp");
    element.textContent = maxAirTemp + "°C - " + location;
}

function getHighestWaterTemp(reservoirs) {
    var maxWaterTemp = 0;
    var location;
    reservoirs.forEach(element => {
        console.log(element.water_temperature);
        if (element.water_temperature > maxWaterTemp) {
            maxWaterTemp = element.water_temperature
            location = element.name;
        }
    });
    var element = document.getElementById("highest-water-temp");
    element.textContent = maxWaterTemp + "°C - " + location;
}

function getBestPressure(reservoirs) {
    var bestPressure = 10000;
    var location;
    reservoirs.forEach(element => {
        console.log(element.pressure);
        if (Math.abs(element.pressure - 1013) < Math.abs(bestPressure - 1013)) {
            bestPressure = element.pressure
            location = element.name;
        }
    });
    var element = document.getElementById("best-pressure");
    element.textContent = bestPressure + " hPa - " + location;
}

function getLowestNoise(reservoirs) {
    var minNoise = 200;
    var location;
    reservoirs.forEach(element => {
        console.log(element.noise_level);
        if (element.noise_level < minNoise) {
            minNoise = element.noise_level
            location = element.name;
        }
    });
    var element = document.getElementById("lowest-noise");
    element.textContent = minNoise + " dB - " + location;
}