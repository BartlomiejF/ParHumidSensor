import requests
import numpy as np

import sds011
import time


if __name__ == "__main__":
    try:
        sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
        sensor.sleep(sleep=False)
        pm2_5 = np.empty(0)
        pm10 = np.empty(0)
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
        print(f"sth went wrong")
