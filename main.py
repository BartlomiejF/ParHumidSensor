from flask import Flask, render_template
from flask_restful import Api
import click
import myapi
import plotter
from db import db, ma
from crontab import CronTab
import pathlib
import argparse


basedir = pathlib.Path(__file__).parent
cron = CronTab(user=False)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    ma.init_app(app)

    if not (basedir/(__file__[:-2]+"sqlite")).exists():
        with app.app_context():
            db.create_all()

    return app


app = create_app()
api = Api(app)

parser = argparse.ArgumentParser(
        prog="ParHumidMonitor",
        description="""Monitor""",
        )

parser.add_argument(
        "--particles",
        help="add particle monitor, give monitor /dev/usbtmc file",
        )

parser.add_argument(
        "--dht",
        help="dht-11 pin number",
        )

args = parser.parse_args()

# if args.cars:
#     api.add_resource(
#         myapi.CarCounter,
#         "/CarCounter"
#         )
#     api.add_resource(
#         myapi.CarCounterLast,
#         "/CarCounter/last"
#         )
#     api.add_resource(
#         myapi.CarCounterLastNumber,
#         "/CarCounter/last/<nb>"
#     )

if args.particles:
    api.add_resource(
        myapi.AirQualityMonitor,
        "/AirQualityMonitor"
        )
    api.add_resource(
        myapi.AirQualityMonitorLast,
        "/AirQualityMonitor/last"
        )
    api.add_resource(
        myapi.AirQualityMonitorLastNumber,
        "/AirQualityMonitor/last/<nb>"
        )
    job = cron.new(command=f"python3 particle_sensor.py {args.particles}")
    job.minute.every(30)
    cron.write()

if args.dht:
    api.add_resource(
        myapi.TempHumidMonitor,
        "/TempHumidMonitor"
        )
    api.add_resource(
        myapi.TempHumidMonitorLast,
        "/TempHumidMonitor/last"
        )
    api.add_resource(
        myapi.TempHumidMonitorLastNumber,
        "/TempHumidMonitor/last/<nb>"
        )
    job = cron.new(command=f"python3 temp_humid_sensor.py {args.dht}")
    job.minute.every(30)
    cron.write()

@app.route("/")
def graphs():
    # carnbdata = myapi.CarCounterLastNumber().get(24).get_json()
    # airqualdata = myapi.AirQualityMonitorLastNumber().get(24).get_json()
    temphumid = myapi.TempHumidMonitor().get().get_json()
    lasttemphumid = myapi.TempHumidMonitorLast().get().get_json()
    lasthumid = lasttemphumid["humidity"]
    lasttemp = lasttemphumid["temperature"]
    airqualdata = myapi.AirQualityMonitor().get().get_json()
    plots = plotter.plot(airqualdata, temphumid)
    return render_template(
        "template2.html",
        temp_humid_plot=plots["temphumid"].decode('utf8'),
        airqual_plot=plots["airqual"].decode('utf8'),
        acttemp=lasttemp,
        acthumid=lasthumid,
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        # host="0.0.0.0"
        )
