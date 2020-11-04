import requests
import adafruit_dht
import board
import digitalio
import time

"""
This is temperature and humidity measurement script. Be sure to use proper GPIO
pin or change it in the script. DHT11 seemed to sometimes fail to read
temperature or humidity so the script tries 20 times to read sensor data.
"""

if __name__ == "__main__":
    # change pin in two below lines:
    digitalio.DigitalInOut(board.D27).direction = digitalio.Direction.INPUT
    sensor = adafruit_dht.DHT11(board.D27)

    temp = None
    humid = None
    for i in range(20):
        try:
            if not humid:
                humid = sensor.humidity
            if not temp:
                temp = sensor.temperature
            print(f"{i}. {time.ctime()}           Temperature: {temp:.1f} Humidity: {humid:.1f}%")
            break
        except RuntimeError:
            print(f"{i}. {time.ctime()}          RuntimeError")
            time.sleep(1)
        except:
            print(f"{i}. {time.ctime()}          sth went wrong")
            time.sleep(1)
    if temp and humid:
        r = requests.post(
            "http://127.0.0.1:5000/TempHumidMonitor",
            params={"temperature": f"{temp:.1f}",
            "humidity": f"{humid:.1f}"},
            )
