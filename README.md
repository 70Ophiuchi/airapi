# AirAPI

# Heroku

* https://airportaircraftapi.herokuapp.com/airplanes

# How to run locally?

* Set the required variables and environment variables in models.py, setup.sh and test_app.py
* One line script:
```
bash setup.sh && pip install -r requirements.txt && flask db init && flask db migrate && flask db upgrade && export FLASK_APP=app.py && flask run --reload
```

* Runs on 127.0.0.1:5000 locally

# Authorization

* Without inputting your own variables:
https://dev-nu0wlq-r.eu.auth0.com/authorize?audience=AirAPI&response_type=token&client_id=OKCBV38vJ2giJX4T6euAndqqmTZjweNu&redirect_uri=http://127.0.0.1/airplanes

* Custom Link (Custom variables):
https://{AUTH0_DOMAIN}}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}

# Endpoints

* /airplanes
    * GET, POST
* /airplanes/<int:id>
    * DELETE, PATCH
* /airports
    * GET, POST
* /airports/<int:id>
    * DELETE, PATCH

* Error Codes and Response

* Unauthorized: 401
* Not Found: 404
* Unprocessable Request: 422
* Internal Server Error: 500
* Response Format (JSON): {
                            'success': False,
                            'error_code': 'error_code',
                            'error_info': 'error_info'
                        }

* Sucessful Request

* Reponse Code: 200
* Response Format (JSON): {
                            'requested_information_title': 'requested_information_body',
                            'success': True
                        }
