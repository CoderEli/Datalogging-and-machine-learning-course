import board
import busio
import sdcardio
import storage
import adafruit_dht
import time
from digitalio import DigitalInOut, Direction, Pull
import analogio

# SD card setup
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = board.GP17
sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Moisture sensor setup
analog_in = analogio.AnalogIn(board.GP26)

def get_voltage(pin):
    return (pin.value * 3.3) / 65535

def get_moisture_percentage():
    min_voltage = 1.7
    max_voltage = 3.3
    
    moisture_voltage  = get_voltage(analog_in)
    
    moisture_percentage = (1 -((moisture_voltage - min_voltage) / (max_voltage - min_voltage))) * 100
    
    return max(0, min(moisture_percentage, 100))


# LED SETUP
led = DigitalInOut(board.GP3)
led.direction = Direction.OUTPUT

# BTN setup
btn = DigitalInOut(board.GP15)
btn.direction = Direction.INPUT
btn.pull= Pull.UP

flag = False

# DHT11 sensor setup
dht_pin = board.GP0
dht = adafruit_dht.DHT11(dht_pin)

previous_state = btn.value
led_state = False
recording = False

# Create CSV header if file doesn't exist
#try:
 
#except OSError:
#    with open("/sd/sensor_data.csv", "w") as f:
#        f.write("timestamp,temperature,humidity\r\n")
number=0


def dhtm_record(number):
    
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        moisture_percentage = get_moisture_percentage()
        
        if temperature is not None and humidity is not None:
            timestamp = time.monotonic()
            #print(f"Temp: {temperature:.1f}°C Humidity: {humidity:.1f}%")
            print(humidity, temperature, moisture_percentage)
            # Append data in CSV format

            with open("/sd/sensor_data"+str(number)+".csv", "a") as f:
                f.write(f"{timestamp},{temperature:.1f},{humidity:.1f},{moisture_percentage:.1f}\r\n")
                
    except RuntimeError as e:
        print(f"Error reading DHT11: {e}")
    

while True:
    current_state = btn.value
    if previous_state and not current_state:
        led_state = not led_state
        led.value = led_state
        number+=1
        filename="/sd/sensor_data"+str(number)+".csv"    
        with open(filename, "w") as f:
            f.write("timestamp,temperature,humidity,moisture\r\n")
    if led_state:
        dhtm_record(number)
    previous_state = current_state
    time.sleep(1)

  
