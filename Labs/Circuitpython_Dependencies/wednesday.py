import board
import busio
import sdcardio
import adafruit_dht
import time
from digitalio import DigitalInOut, Direction, Pull


# LED SETUP
led_1 = DigitalInOut(board.GP16)
led_1.direction = Direction.OUTPUT

led_2 = DigitalInOut(board.GP17)
led_2.direction = Direction.OUTPUT

led_3 = DigitalInOut(board.GP18)
led_3.direction = Direction.OUTPUT

led_4 = DigitalInOut(board.GP19)
led_4.direction = Direction.OUTPUT

flag = False

# DHT11 sensor setup
dht_pin = board.GP0
dht = adafruit_dht.DHT11(dht_pin)

led_state = False
recording = False

# Create CSV header if file doesn't exist

def dht_record():
    
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        
        if temperature is not None and humidity is not None:
            timestamp = time.monotonic()
            #print(f"Temp: {temperature:.1f}°C Humidity: {humidity:.1f}%")
            print(humidity, temperature)
                
    except RuntimeError as e:
        print(f"Error reading DHT11: {e}")
    

while True:
    dht_record()
    time.sleep(0.05)
    led_3.value = True

  
