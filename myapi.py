from flask_restful import Resource, reqparse
import datetime
from flask import jsonify
from db import CarCount, db, AirParameters, CarCountSchema, AirParametersSchema
from db import TempAndHumidity, TempAndHumiditySchema


parser = reqparse.RequestParser()
parser.add_argument("carnb")
parser.add_argument("pm2_5")
parser.add_argument("pm10")
parser.add_argument("humidity")
parser.add_argument("temperature")


class CarCounter(Resource):
    def get(self):
        all_data = CarCount.query.all()
        schema = CarCountSchema(only=("date_time", "number"), many=True)
        return jsonify(schema.dump(all_data))

    def post(self):
        args = parser.parse_args()
        date = datetime.datetime.now()
        carcount = CarCount(date_time=date, number=args["carnb"])
        db.session.add(carcount)
        db.session.commit()
        return {"Message": "Added car counter data."}


class CarCounterLast(Resource):
    def get(self):
        data = CarCount.query.order_by(CarCount.id.desc()).first()
        schema = CarCountSchema(only=("date_time", "number"))
        return jsonify(schema.dump(data))


class CarCounterLastNumber(Resource):
    def get(self, nb):
        data = CarCount.query.order_by(CarCount.id.desc())
        maxnb = data.count()
        if int(nb) > maxnb:
            nb = maxnb
        limited = data.limit(nb)
        schema = CarCountSchema(only=("date_time", "number"), many=True)
        return jsonify(schema.dump(limited))


class AirQualityMonitor(Resource):
    def get(self):
        data = AirParameters.query.all()
        schema = AirParametersSchema(
            only=("pm2_5", "pm10", "date_time"),
            many=True,
            )
        return jsonify(schema.dump(data))

    def post(self):
        args = parser.parse_args()
        date = datetime.datetime.now()
        airquality = AirParameters(
            date_time=date,
            pm2_5=args.get("pm2_5"),
            pm10=args.get("pm10"),
            )
        db.session.add(airquality)
        db.session.commit()
        return {"Message": "Added air quality parameters."}


class AirQualityMonitorLast(Resource):
    def get(self):
        data = AirParameters.query.order_by(
            AirParameters.id.desc()
            ).first()
        schema = AirParametersSchema(only=("pm2_5", "pm10", "date_time"))
        return jsonify(schema.dump(data))


class AirQualityMonitorLastNumber(Resource):
    def get(self, nb):
        data = AirParameters.query.order_by(AirParameters.id.desc())
        maxnb = data.count()
        if int(nb) > maxnb:
            nb = maxnb
        limited = data.limit(nb)
        schema = AirParametersSchema(
            many=True,
            only=("pm2_5", "pm10", "date_time")
            )
        return jsonify(schema.dump(limited))


class TempHumidMonitor(Resource):
    def get(self):
        data = TempAndHumidity.query.all()
        schema = TempAndHumiditySchema(
            only=("humidity", "temperature", "date_time"),
            many=True)
        return jsonify(schema.dump(data))

    def post(self):
        args = parser.parse_args()
        date = datetime.datetime.now()
        temphumid = TempAndHumidity(
            date_time=date,
            humidity=args.get("humidity"),
            temperature=args.get("temperature"),
            )
        db.session.add(temphumid)
        db.session.commit()
        return {"Message": "Added air quality parameters."}


class TempHumidMonitorLast(Resource):
    def get(self):
        data = TempAndHumidity.query.order_by(
            TempAndHumidity.id.desc()
            ).first()
        schema = TempAndHumiditySchema(
            only=("humidity", "temperature", "date_time")
            )
        return jsonify(schema.dump(data))


class TempHumidMonitorLastNumber(Resource):
    def get(self, nb):
        data = TempAndHumidity.query.order_by(TempAndHumidity.id.desc())
        maxnb = data.count()
        if int(nb) > maxnb:
            nb = maxnb
        limited = data.limit(nb)
        schema = TempAndHumiditySchema(
            many=True,
            only=("humidity", "temperature", "date_time")
            )
        return jsonify(schema.dump(limited))
