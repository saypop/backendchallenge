# app/__init__.py

from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Car

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/cars/', methods=['POST', 'GET'])
    def cars():
        if request.method == 'POST':
            make = str(request.data.get('make', ''))
            model = str(request.data.get('model', ''))
            year = request.data.get('year', '')
            if make and model and year:
                car = Car(make=make, model=model, year=year)
                car.save()
                response: object = jsonify({
                    'id': car.id,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year
                })
                response.status_code = 201
                return response
        else:
            all_cars = Car.get_all()
            results = []
            for car in all_cars:
                obj = {
                    'id': car.id,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year
                }
                results.append(obj)
            response: object = jsonify(results)
            response.status_code = 200
            return response

    return app
