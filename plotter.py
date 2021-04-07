import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def plot(airqualjson=None, temphumidjson=None):
    # carnb_data = pd.DataFrame.from_dict(carnbjson)
    figdata_airqual_png = None
    figdata_temphumid_png = None

    if airqualjson is not None:
        airqual_data = pd.DataFrame.from_dict(airqualjson)
        airqual_time = airqual_data["date_time"].astype("datetime64")

        fig_airqual, ax_airqual = plt.subplots(1, 2, figsize=(10, 5))
        ax_airqual[0].plot(airqual_time, airqual_data["pm2_5"])
        ax_airqual[0].axhline(20, ls="--", c="r")
        ax_airqual[0].axhspan(0, 20, 0, 1, color="g", alpha=0.2)
        ax_airqual[0].set_title("pm 2.5")
        axymax = airqual_data["pm2_5"].max()
        axymax = axymax*1.1
        if axymax > 20:
            ax_airqual[0].axhspan(20, axymax, 0, 1, color="r", alpha=0.2)

        ax_airqual[1].plot(airqual_time, airqual_data["pm10"])
        ax_airqual[1].axhline(50, ls="--", c="r")
        ax_airqual[1].axhspan(0, 50, 0, 1, color="g", alpha=0.2)
        ax_airqual[1].set_title("pm 10")
        ax1ymax = airqual_data["pm10"].max()
        ax1ymax = ax1ymax*1.1
        if ax1ymax > 50:
            ax_airqual[1].axhspan(50, ax1ymax, 0, 1, color="r", alpha=0.2)

        figfile_airqual = BytesIO()
        fig_airqual.savefig(figfile_airqual, format='png')
        figfile_airqual.seek(0)  # rewind to beginning of file
        figdata_airqual_png = figfile_airqual.getvalue()  # extract string (stream of bytes)
        figdata_airqual_png = base64.b64encode(figdata_airqual_png)


    if temphumidjson is not None:
        temphumid_data = pd.DataFrame.from_dict(temphumidjson)
        temphumid_time = temphumid_data["date_time"].astype("datetime64")

        fig_temphumid, ax_temphumid = plt.subplots(1, 2, figsize=(10, 5))
        ax_temphumid[0].plot(temphumid_time, temphumid_data["temperature"])
        ax_temphumid[1].plot(temphumid_time, temphumid_data["humidity"])

        figfile_temphumid = BytesIO()
        fig_temphumid.savefig(figfile_temphumid, format='png')
        figfile_temphumid.seek(0)  # rewind to beginning of file
        figdata_temphumid_png = figfile_temphumid.getvalue()  # extract string (stream of bytes)
        figdata_temphumid_png = base64.b64encode(figdata_temphumid_png)

    return {"airqual": figdata_airqual_png,
            "temphumid": figdata_temphumid_png,}
