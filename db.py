from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


class CarCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    number = db.Column(db.Integer)


class AirParameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    pm2_5 = db.Column(db.Float)
    pm10 = db.Column(db.Float)


class TempAndHumidity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    comment = db.Column(db.String(30))


class CarCountSchema(ma.ModelSchema):
    class Meta:
        model = CarCount


class AirParametersSchema(ma.ModelSchema):
    class Meta:
        model = AirParameters


class TempAndHumiditySchema(ma.ModelSchema):
    class Meta:
        model = TempAndHumidity
