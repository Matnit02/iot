let airTempGauge, waterTempGauge, pressureGauge, noiseLevelGauge, lightIntensityGauge, pm1_0Gauge, pm2_5Gauge, pm10Gauge;

document.addEventListener("DOMContentLoaded", function() {
    // Initialize each gauge
    airTempGauge = new JustGage({
        id: "airTempGauge",
        value: -50,  // Initial dummy value
        min: -50,
        max: 50,
        title: "",
        label: "°C",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0",
    });

    waterTempGauge = new JustGage({
        id: "waterTempGauge",
        value: 0,
        min: 0,
        max: 40,
        title: "",
        label: "°C",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0",
        levelColors: ["#e3e5db", "#81cbea", "#0693f8"]
    });

    pressureGauge = new JustGage({
        id: "pressureGauge",
        value: 0,
        min: 900,
        max: 1100,
        title: "",
        label: "hPa",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0",
        levelColors: ["#e3e5db", "#80ee7b", "#0fee05"]
    });

    humidityGauge = new JustGage({
        id: "humidityGauge",
        value: 0,
        min: 0,
        max: 100,
        title: "",
        label: "%",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0"
    });

    lightIntensityGauge = new JustGage({
        id: "lightIntensityGauge",
        value: 0,
        min: 0,
        max: 65535,
        title: "",
        label: "lx",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0",
        levelColors: ["#0c12c2", "#deca95", "#d1b25c"]
    });

    pm1_0Gauge = new JustGage({
        id: "pm1_0Gauge",
        value: 0,
        min: 0,
        max: 300,
        title: "",
        label: "µg/m³",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0"
    });

    pm2_5Gauge = new JustGage({
        id: "pm2_5Gauge",
        value: 0,
        min: 0,
        max: 300,
        title: "",
        label: "µg/m³",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0"
    });

    pm10Gauge = new JustGage({
        id: "pm10Gauge",
        value: 0,
        min: 0,
        max: 300,
        title: "",
        label: "µg/m³",
        pointer: true,
        gaugeWidthScale: 0.8,
        gaugeColor: "#f0f0f0"
    });
});

// Function to update each gauge with new data
function updateGauge(gaugeId, newValue) {
    switch(gaugeId) {
        case 'airTempGauge':
            airTempGauge.refresh(newValue);
            break;
        case 'waterTempGauge':
            waterTempGauge.refresh(newValue);
            break;
        case 'pressureGauge':
            pressureGauge.refresh(newValue);
            break;
        case 'humidityGauge':
            humidityGauge.refresh(newValue);
            break;
        case 'lightIntensityGauge':
            lightIntensityGauge.refresh(newValue);
            break;
         case 'pm1_0Gauge':
            pm1_0Gauge.refresh(newValue);
            break;
        case 'pm2_5Gauge':
            pm2_5Gauge.refresh(newValue);
            break;
        case 'pm10Gauge':
            pm10Gauge.refresh(newValue);
            break;   
        default:
            console.warn(`Unknown gauge ID: ${gaugeId}`);
    }
}
