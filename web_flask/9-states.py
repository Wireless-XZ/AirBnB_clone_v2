#!/usr/bin/python3
"""This module starts a Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display HTML page for all states sorted by name."""
    states = sorted(storage.all('State').values(), key=lambda s: s.name)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Display HTML page for state and its cities."""
    
    state = None
    for s in storage.all('State').values():
        if s.id == id:
            state = s
            break
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
