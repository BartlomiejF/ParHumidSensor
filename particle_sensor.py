import requests
import numpy as np
import sds011
import time

"""
This script measures PM2.5 and PM10 concentration with SDS011 sensor. When
executed the script launches SDS011 fan and lets it work for 90 seconds to
make shure that the sensor measurement is filled with recent air in maximum
volume. It also makes 5 measurements and calculates mean value to minimize
some errors.
"""

if __name__ == "__main__":
    try:
        sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
        sensor.sleep(sleep=False)
        pm2_5 = np.empty(0)
        pm10 = np.empty(0)
        time.sleep(60)
        for _ in range(5):
            time.sleep(30)
            meas = sensor.query()
            pm2_5 = np.append(pm2_5, meas[0])
            pm10 = np.append(pm10, meas[1])
            time.sleep(2)
        pm2_5 = pm2_5[1:].mean()
        pm10 = pm10[1:].mean()
        sensor.sleep()
        sensor.ser.close()
        r = requests.post(
            "http://127.0.0.1:5000/AirQualityMonitor",
            params={"pm2_5": f"{pm2_5:.2f}", "pm10": f"{pm10:.2f}"}
            )

    except:
        print("sth went wrong")
