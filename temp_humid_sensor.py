import requests
import numpy as np
import adafruit_dht
import board
import argparse
import time

if __name__ == "__main__":
    try:
        sensor = adafruit_dht.DHT11(board.D7)

        humid, temp = sensor.humidity, sensor.temperature

        r = requests.post(
            "http://127.0.0.1:5000//TempHumidMonitor",
            params={
                "temperature": f"{temp:.1f}",
                "humidity": f"{humid:.1f}"
                },
            )

        print(f"{time.ctime()}           Temperature: {temp:.1f} Humidity: {humid:.1f}%")

    except:
        print(f"{time.ctime()}           sth went wrong")
