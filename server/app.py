# server/app.py

from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Pet

# create a Flask application instance
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)


@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    pet = Pet(name=data['name'], species=data['species'])
    db.session.add(pet)
    db.session.commit()
    return jsonify({'id': pet.id, 'name': pet.name, 'species': pet.species}), 201


@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'species': p.species} for p in pets])


if __name__ == '__main__':
    app.run(port=5555, debug=True)
