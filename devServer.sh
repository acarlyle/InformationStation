sudo service mysql start
export FLASK_CONFIG=development
export FLASK_APP=run.py
flask run --host '0.0.0.0' --port 8080
