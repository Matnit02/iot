import time
import board
import busio
import bmp180

# Inicjalizacja I2C i czujnika BMP180
i2c = board.I2C()
sensor = bmp180.BMP180(i2c)

# Opcjonalnie: ustawienie trybu oversampling
sensor.oversampling = 2  # Możesz wybrać wartość od 0 do 3 (0 = szybkie, 3 = dokładne)

# Wysokość nad poziomem morza w metrach (zmień na swoją lokalizację)
wysokosc_nad_poziomem_morza = 383 # bo krk jest 383npm

def koryguj_cisnienie(cisnienie, wysokosc):
    """Przelicza ciśnienie bezwzględne na ciśnienie na poziomie morza."""
    return cisnienie / (1 - (wysokosc / 44330.0))**5.255

print("Rozpoczynam odczyt z BMP180...")
while True:
    try:
        # Odczyt temperatury i ciśnienia
        temperatura = sensor.temperature
        cisnienie_bezwzgledne = sensor.pressure
        cisnienie_na_poziomie_morza = koryguj_cisnienie(cisnienie_bezwzgledne, wysokosc_nad_poziomem_morza)

        print(f"Temperatura: {temperatura:.2f} °C")
        print(f"Ciśnienie bezwzględne: {cisnienie_bezwzgledne:.2f} hPa")
        print(f"Ciśnienie na poziomie morza: {cisnienie_na_poziomie_morza:.2f} hPa")
        time.sleep(1)  # Odczekaj sekundę przed kolejnym odczytem
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        break
