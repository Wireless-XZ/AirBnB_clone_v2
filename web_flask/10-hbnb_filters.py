from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)

# Define route for the HBNB filters page
@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    # Get all states and amenities from the database, sorted by name
    states = sorted(storage.all('State').values(), key=lambda state: state.name)
    amenities = sorted(storage.all('Amenity').values(), key=lambda amenity: amenity.name)
    # Render the template with the state and amenity variables passed in
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)

# Define a function to close the database connection after each request
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == '__main__':
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)
