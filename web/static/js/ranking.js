function getHighestAirTemp(reservoirs) {
    var maxAirTemp = 0;
    var location;
    reservoirs.forEach(element => {
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
        if (Math.abs(element.pressure - 1013) < Math.abs(bestPressure - 1013)) {
            bestPressure = element.pressure
            location = element.name;
        }
    });
    var element = document.getElementById("best-pressure");
    element.textContent = bestPressure + " hPa - " + location;
}

function getLowestHumidity(reservoirs) {
    var minHumidity = 200;
    var location;
    reservoirs.forEach(element => {
        if (element.humidity < minHumidity) {
            minHumidity = element.humidity
            location = element.name;
        }
    });
    var element = document.getElementById("lowest-humidity");
    element.textContent = minHumidity + " % - " + location;
}

function getHighestLightIntensity(reservoirs) {
    var maxIntensity = 0;
    var location;
    reservoirs.forEach(element => {
        if (element.light_intensity > maxIntensity) {
            maxIntensity = element.light_intensity
            location = element.name;
        }
    });
    var element = document.getElementById("highest-intensity");
    element.textContent = maxIntensity + " lx - " + location;
}

function getLowestPm1_0(reservoirs) {
    var minPm1_0 = 10000;
    var location;
    reservoirs.forEach(element => {
        if (element.pm1_0 < minPm1_0) {
            minPm1_0 = element.pm1_0
            location = element.name;
        }
    });
    var element = document.getElementById("lowest-pm1_0");
    element.textContent = minPm1_0 + " µg/m3 - " + location;
}

function getLowestPm2_5(reservoirs) {
    var minPm2_5 = 10000;
    var location;
    reservoirs.forEach(element => {
        if (element.pm2_5 < minPm2_5) {
            minPm2_5 = element.pm2_5
            location = element.name;
        }
    });
    var element = document.getElementById("lowest-pm2_5");
    element.textContent = minPm2_5 + " µg/m3 - " + location;
}

function getLowestPm10(reservoirs) {
    var minPm10 = 10000;
    var location;
    reservoirs.forEach(element => {
        if (element.pm10 < minPm10) {
            minPm10 = element.pm10
            location = element.name;
        }
    });
    var element = document.getElementById("lowest-pm10");
    element.textContent = minPm10 + " µg/m3 - " + location;
}