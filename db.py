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


class CarCountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarCount
        load_instance = True


class AirParametersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AirParameters
        load_instance = True


class TempAndHumiditySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TempAndHumidity
        load_instance = True
