import os
from typing import final
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import requires_auth
from models import *

ITEMS_PER_PAGE = 10

def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * ITEMS_PER_PAGE
  end = start + ITEMS_PER_PAGE

  query = [item.format() for item in selection]
  paginated_query = query[start:end]
  return paginated_query

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route('/airplanes', methods=["GET"])
  def get_airplanes():
    airplanes = Airplanes.query.order_by(Airplanes.id).all()
    airplanes_paginated = paginate(request, airplanes)
    return jsonify({
      'airplanes': airplanes_paginated,
      'total': len(airplanes),
      'success': True
    })

  @app.route('/airplanes/<int:id>', methods=["GET", "DELETE"])
  def get_specific_airplane(id):

    airplane = Airplanes.query.filter_by(id=id).one_or_none()
    return jsonify({
      'airplane': airplane,
      'success': True
    })

  @app.route('/airports', methods=['GET'])
  def get_airports():
    airports = Airports.query.order_by().all()
    airports_paginated = paginate(request, airports)
    return jsonify({
      'airports': airports_paginated,
      'total': len(airports),
      'success': True
    })
  @app.route('/airports/<int:id>', methods=['GET'])
  def get_specific_airport(id):
    airport = Airports.query.filter_by(id=id).one_or_none()
    return jsonify({
      'airport': airport,
      'success': True
    })

  @app.route('/airports', methods=["POST"])
  @requires_auth('add:airport')
  def add_airport():
    body = request.get_json()

    airport_name = body.get('name', None)
    airport_code = body.get('code', None)
    airport_country = body.get('country', None)

    new_airport = Airports(airport_name=airport_name,
                           airport_code=airport_code,
                           airport_country=airport_country
                          )
    error = False
    try:
      new_airport.insert()
    except:
      error = True
    finally:
      db.session.close()
      if error == False:
          return jsonify({
            'success': True,
          })
      else:
        abort(401)
  
  @app.route('/airplanes', methods=["POST"])
  @requires_auth('add:airplane')
  def add_airplane():
    body = request.get_json()

    airplane_name = body.get('name', None)
    airplane_manufacturer = body.get('manufacturer', None)
    airplane_built_in = body.get('built_in', None)

    new_airplane = Airplanes(airplane_name=airplane_name,
                           airplane_manufacturer=airplane_manufacturer,
                           airplane_built_in=airplane_built_in
                          )
    error = False
    try:
      new_airplane.insert()
    except:
      error = True
    finally:
      db.session.close()
      if error == False:
          return jsonify({
            'success': True,
          })
      else:
        abort(401)

  @app.route('/airplanes/<int:id>', methods=["DELETE"])
  @requires_auth('delete:airplane')
  def delete_airplane(id):
    airplane = Airplanes(id=id)
    error = False
    try:
      airplane.delete()
    except:
      error = True
    finally:
      db.session.close()
      if not error:
        return jsonify({
          'success': True,
          'deleted_airplane_id': id
        })
      else:
        abort(401)

  @app.route('/airports/<int:id>', methods=["DELETE"])
  @requires_auth('delete:airport')
  def delete_airplane(id):
    airport = Airports(id=id)
    error = False
    try:
      airport.delete()
    except:
      error = True
    finally:
      db.session.close()
      if not error:
        return jsonify({
          'success': True,
          'deleted_airport_id': id
        })
      else:
        abort(401)

  @app.route('/airports/<int:id>', methods=["PATCH"])
  @requires_auth('update:airport')
  def patch_airport(id):
    body = request.get_json()

    patched_airport = Airports(name=body.name, code=body.code, country=body.country)
    error = False

    try:
      patched_airport.update()
    except:
      error = True
    finally:
      db.session.close()
      if not error:
        return jsonify({
          'success': True,
          'updated_airport': id
        })
      else:
        abort(401)

  @app.route('/airplane/<int:id>', methods=["PATCh"])
  @requires_auth('update:airplane')
  def patch_airplane(id):
    body = request.get_json()

    patched_airplane = Airplanes(name=body.name, code=body.code, country=body.country)
    error = False

    try:
      patched_airplane.update()
    except:
      error = True
    finally:
      db.session.close()
      if not error:
        return jsonify({
          'success': True,
          'updated_airplane': id
        })
      else:
        abort(401)

  @app.errorhandler(404)
  def not_found():
      return jsonify({'success': False,
                      'message': 'Resource was not found on the server'
                      , 'error_code': 404})

  @app.errorhandler(422)
  def unprocessable():
      return jsonify({'success': False,
                      'message': 'Request could not be processed',
                      'error_code': 422})

  @app.errorhandler(400)
  def bad_request():
      return jsonify({'success': False, 'message': 'Bad request',
                      'error_code': 400})

  @app.errorhandler(405)
  def method_not_allowed():
      return jsonify({'success': False,
                      'message': 'Method is not allowed on requested resource'
                      , 'error_code': 405})

  @app.errorhandler(408)
  def request_timeout():
      return jsonify({'success': False, 'message': 'Request timed out'
                      , 'error_code': 408})

  @app.errorhandler(500)
  def server_error():
      return jsonify({'success': False,
                      'message': 'Internal Server Error',
                      'error_code': 500})

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)