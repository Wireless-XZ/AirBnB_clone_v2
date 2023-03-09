#!/usr/bin/python3
""" cities_by_states module """
from flask import Flask, render_template
from models import storage, State, City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Removes the current SQLAlchemy Session after each request"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with a list of all states and their cities"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda s: s.name)

    return render_template('cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
