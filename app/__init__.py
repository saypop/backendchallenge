# app/__init__.py

from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import json

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Cars, Branches, Drivers

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/cars/', methods=['POST', 'GET'])
    def cars_methods():
        if request.method == 'POST':
            make = str(request.data.get('make', ''))
            model = str(request.data.get('model', ''))
            year = request.data.get('year', '')
            if make and model and year:
                car = Cars(make=make, model=model, year=year)
                car.save()
                response: object = jsonify({
                    'id': car.id,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year,
                    'currently_with': car.currently_with
                })
                response.status_code = 201
                return response
        elif request.method == 'GET':
            all_cars = Cars.get_all()
            results = []
            for car in all_cars:
                obj = {
                    'id': car.id,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year,
                    'currently_with': car.currently_with
                }
                results.append(obj)
            response: object = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/cars/<int:id>', methods=['GET', 'PUT'])
    def car_methods(id, **kwargs):
        car = Cars.query.filter_by(id=id).first()

        if not car:
            abort(404)

        if request.method == 'GET':
            response: object = jsonify({
                'id': car.id,
                'make': car.make,
                'model': car.model,
                'year': car.year,
                'currently_with': car.currently_with
            })
            response.status_code = 200
            return response
        elif request.method == 'PUT':
            for key, value in request.data.items():
                setattr(car, key, value)
            car.save()
            response: object = jsonify({
                'id': car.id,
                'make': car.make,
                'model': car.model,
                'year': car.year,
                'currently_with': car.currently_with
            })
            response.status_code = 200
            return response

    @app.route('/branches/', methods=['POST', 'GET'])
    def branches_methods():
        if request.method == 'POST':
            city = str(request.data.get('city', ''))
            postcode = str(request.data.get('postcode', ''))
            if city and postcode:
                branch = Branches(city=city, postcode=postcode)
                branch.save()
                response: object = jsonify({
                    'id': branch.id,
                    'city': branch.city,
                    'postcode': branch.postcode
                })
                response.status_code = 201
                return response
        elif request.method == 'GET':
            all_branches = Branches.get_all()
            results = []
            for branch in all_branches:
                obj = {
                    'id': branch.id,
                    'city': branch.city,
                    'postcode': branch.postcode
                }
                results.append(obj)
            response: object = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/branches/<int:id>', methods=['GET'])
    def branch_methods(id, **kwargs):
        branch = Branches.query.filter_by(id=id).first()

        if not branch:
            abort(404)

        if request.method == 'GET':
            response: object = jsonify({
                'id': branch.id,
                'city': branch.city,
                'postcode': branch.postcode
            })
            response.status_code = 200
            return response

    @app.route('/drivers/', methods=['POST', 'GET'])
    def drivers_methods():
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            dob = str(request.data.get('dob', ''))
            if name and dob:
                driver = Drivers(name=name, dob=dob)
                driver.save()
                response: object = jsonify({
                    'id': driver.id,
                    'name': driver.name,
                    'dob': driver.dob
                })
                response.status_code = 201
                return response
        elif request.method == 'GET':
            all_drivers = Drivers.get_all()
            results = []
            for driver in all_drivers:
                obj = {
                    'id': driver.id,
                    'name': driver.name,
                    'dob': driver.dob
                }
                results.append(obj)
            response: object = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/drivers/<int:id>', methods=['GET'])
    def driver_methods(id, **kwargs):
        driver = Drivers.query.filter_by(id=id).first()

        if not driver:
            abort(404)

        if request.method == 'GET':
            response: object = jsonify({
                'id': driver.id,
                'name': driver.name,
                'dob': driver.dob
            })
            response.status_code = 200
            return response

    @app.route('/cars/<int:car_id>/drivers/<int:driver_id>', methods=['PUT'])
    def assign_driver(car_id, driver_id):
        car = Cars.query.filter_by(id=car_id).first()
        driver = Drivers.query.filter_by(id=driver_id).first()

        if not car and driver:
            abort(404)

        car.currently_with = json.dumps(driver.__repr__())
        car.save()

        response: object = jsonify({
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'currently_with': car.currently_with
        })
        response.status_code = 200
        return response

    @app.route('/cars/<int:car_id>/branches/<int:branch_id>', methods=['PUT'])
    def assign_branch(car_id, branch_id):
        car = Cars.query.filter_by(id=car_id).first()
        branch = Branches.query.filter_by(id=branch_id).first()

        if not car and branch:
            abort(404)

        car.currently_with = json.dumps(branch.__repr__())
        car.save()

        response: object = jsonify({
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'currently_with': car.currently_with
        })
        response.status_code = 200
        return response


    return app
