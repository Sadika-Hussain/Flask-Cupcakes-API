"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

# Application configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'oh-so-secret'

# Debug Toolbar
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Database setup
connect_db(app)
db.create_all()


@app.route('/api/cupcakes')
def list_cupcakes():
    """Get a list of all cupcakes.
    
    Fetches all cupcake records from the database and returns
    them as JSON.

    Returns:
        A JSON response containing a list of serialized cupcakes.
    """
    all_cupcakes = Cupcake.query.all()

    serialized = [cupcake.serialize() for cupcake in all_cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get details of a specific cupcake by its ID.

    Returns:
        A JSON response containing the serialized data of the cupcake.
        Returns a 404 error if the cupcake is not found.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    """Create a new cupcake.
    
    Reads cupcake details from a JSON request and creates a new
    cupcake record in the database.

    Returns:
        A JSON response containing the serialized data of the newly created cupcake
        along with a 201 status code.
    """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] 

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return ( jsonify(cupcake=serialized), 201 )

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a specific cupcake.
    
    Updates the cupcake record with the given ID using the data
    provided in the JSON request.

    Returns:
        A JSON response containing the serialized data of the updated cupcake.
        Returns a 404 error if the cupcake is not found.
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a specific cupcake.
    
    Deletes the cupcake record with the given ID from the database.

    Returns:
        A JSON response with a message confirming the deletion.
    """
    Cupcake.query.filter_by(id=cupcake_id).delete()
    db.session.commit()
    return jsonify(message='Deleted')

@app.route('/')
def home_page():
    """Flask route to render the homepage containing cupcake info. """
    return render_template('index.html')