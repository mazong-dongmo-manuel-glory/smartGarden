import smbus
import time
from gpiozero import LED

# --- I2C / ADC PCF8591 ---
bus = smbus.SMBus(1)
addr = 0x4B  # Adresse I2C du PCF8591 (config.py: ADC_ADDRESS)

# --- LEDs (BCM GPIO, selon config.py) ---
# PIN_LED_GREEN  = 16
# PIN_LED_ORANGE =  6
# PIN_LED_RED    =  5
led_green  = LED(16)
led_orange = LED(6)
led_red    = LED(5)

def read_adc(channel):
    """Lit la valeur analogique du canal ADC du PCF8591."""
    command = 0x84 | (channel << 4)
    bus.write_byte(addr, command)
    return bus.read_byte(addr)

print("Test pluie + humidité sol")

while True:
    rain = read_adc(0)   # A0 → Capteur pluie (config.py: RAIN_ADC_CHANNEL = 0)
    soil = read_adc(1)   # A1 → Humidité du sol (config.py: PIN_SOIL = 1)

    print(f"Pluie: {rain}  | Sol: {soil}")

    # Éteindre toutes les LEDs d'abord
    led_green.off()
    led_orange.off()
    led_red.off()

    # --- Logique de la LED selon le niveau de pluie ---
    if rain < 80:
        led_green.on()      # Pas de pluie → vert
    elif rain < 150:
        led_orange.on()     # Pluie légère → orange (anciennement jaune)
    else:
        led_red.on()        # Forte pluie → rouge

    time.sleep(1)
