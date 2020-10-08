import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import myapi


def plot(airqualjson, temphumidjson):
    # carnb_data = pd.DataFrame.from_dict(carnbjson)
    airqual_data = pd.DataFrame.from_dict(airqualjson)
    temphumid_data = pd.DataFrame.from_dict(temphumidjson)

    airqual_time = airqual_data["date_time"].astype("datetime64")
    temphumid_time = temphumid_data["date_time"].astype("datetime64")
    
    fig_airqual, ax_airqual = plt.subplots(1,2, figsize=(10, 5))
    ax_airqual[0].plot(airqual_time, airqual_data["pm2_5"])
    ax_airqual[0].axhline(20, ls="--", c="r")
    ax_airqual[0].axhspan(0, 20, 0, 1, color="g", alpha=0.2)
    axymax = airqual_data["pm2_5"].max()
    axymax = axymax*1.1
    ax_airqual[0].axhspan(20, axymax, 0, 1, color="r", alpha=0.2)

    ax_airqual[1].plot(airqual_time, airqual_data["pm10"])
    ax_airqual[1].axhline(50, ls="--", c="r")
    ax_airqual[1].axhspan(0, 50, 0, 1, color="g", alpha=0.2)
    ax1ymax = airqual_data["pm10"].max()
    ax1ymax = ax1ymax*1.1
    ax_airqual[1].axhspan(50, ax1ymax, 0, 1, color="r", alpha=0.2)

    fig_temphumid, ax_temphumid = plt.subplots(1,2, figsize=(10, 5))
    ax_temphumid[0].plot(temphumid_time, temphumid_data["temperature"])
    ax_temphumid[1].plot(temphumid_time, temphumid_data["humidity"])

    figfile_airqual = BytesIO()
    figfile_temphumid = BytesIO()
    fig_airqual.savefig(figfile_airqual, format='png')
    fig_temphumid.savefig(figfile_temphumid, format='png')
    figfile_airqual.seek(0)  # rewind to beginning of file
    figfile_temphumid.seek(0)  # rewind to beginning of file
    figdata_airqual_png = figfile_airqual.getvalue()  # extract string (stream of bytes)
    figdata_temphumid_png = figfile_temphumid.getvalue()  # extract string (stream of bytes)
    figdata_airqual_png = base64.b64encode(figdata_airqual_png)
    figdata_temphumid_png = base64.b64encode(figdata_temphumid_png)
    
    return (figdata_airqual_png, figdata_temphumid_png)