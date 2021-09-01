from flask import Flask, json, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    


## HTTP GET - Read Record

# get random cafe from database with jsonify
@app.route('/random')
def random_cafe():
    cafes = Cafe.query.all()
    chosen_cafe = random.choice(cafes)

    cafe_json = {

        'cafe': {
            'name': chosen_cafe.name,
            'map_url': chosen_cafe.map_url,
            'img_url': chosen_cafe.img_url,
            'location': chosen_cafe.location,
            'seats': chosen_cafe.seats,

            'amenities': {
                'has_toilet': chosen_cafe.has_toilet,
                'has_wifi': chosen_cafe.has_wifi,
                'has_sockets': chosen_cafe.has_sockets,
                'can_take_calls': chosen_cafe.can_take_calls
            },

            'coffee_price': chosen_cafe.coffee_price
        }

    }

    return jsonify(cafe_json)


# get all cafes in database with jsonify
# TURNS OUT I CAN USE tableInstance.to_dict *facepalm*
@app.route('/all')
def all_cafes():
    cafes = Cafe.query.all()

    cafes_to_return = {
        'cafes': []
    }

    for cafe in cafes:
        to_append = {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,

            'amenities': {
                'has_toilet': cafe.has_toilet,
                'has_wifi': cafe.has_wifi,
                'has_sockets': cafe.has_sockets,
                'can_take_calls': cafe.can_take_calls
            },

            'coffee_price': cafe.coffee_price
        }

        cafes_to_return['cafes'].append(to_append)


    return jsonify(cafes_to_return)


# give cafes with the location specified
@app.route('/search')
def search_cafe():
    location = request.args.get('loc')

    cafes = Cafe.query.filter_by(location=location).all()

    if len(cafes) != 0:
        cafes_to_return = {
            'cafes': []
        }

        for cafe in cafes:
            to_append = {
                'id': cafe.id,
                'name': cafe.name,
                'map_url': cafe.map_url,
                'img_url': cafe.img_url,
                'location': cafe.location,
                'seats': cafe.seats,

                'amenities': {
                    'has_toilet': cafe.has_toilet,
                    'has_wifi': cafe.has_wifi,
                    'has_sockets': cafe.has_sockets,
                    'can_take_calls': cafe.can_take_calls
                },

                'coffee_price': cafe.coffee_price
            }

            cafes_to_return['cafes'].append(to_append)
        
        return jsonify(cafes_to_return)

    return jsonify({'error': {'Not Found': "Sorry, we don't have a cafe at that location."}})



## HTTP POST - Create Record

# adds cafe to database
@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('has_toilet')),
        has_wifi=bool(request.form.get('has_wifi')),
        has_sockets=bool(request.form.get('has_sockets')),
        can_take_calls=bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price')
    )

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({'response': {'success': 'Successfully added the new cafe.'}})



## HTTP PUT/PATCH - Update Record

# updates price of a single cafe in a database with specified id
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()

    if cafe != None:
        cafe.price = request.args.get('new_price')
        db.session.commit()     # DON'T FORGET TO COMMIT EVERY CHANGE!

        return jsonify({'success': 'Successfully updated the price.'}), 200

    return jsonify({'error': {'Not Found': 'Sorry, a cafe with that id was not found in the database.'}}), 404



## HTTP DELETE - Delete Record

# deletes specified cafe from database given that api_key matches
@app.route('/report-close/<int:cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()

    if cafe != None and request.args.get('api_key') == "TopSecretAPIKey":
        db.session.delete(cafe)
        db.session.commit()

        return jsonify({'success': 'The specified cafe has been deleted successfully.'}), 200

    elif request.args.get('api_key') != "TopSecretAPIKey":
        return jsonify({'error': "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

    return jsonify({"error": {"Not Found": "Sorry, a cafe with that id was not found in the database."}}), 403



if __name__ == '__main__':
    app.run(debug=True)