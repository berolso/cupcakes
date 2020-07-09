"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm
from flask_cors import CORS
from sqlalchemy import func




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

CORS(app)

# from forms import AddCupcakeForm

# custom 404
@app.errorhandler(404)
def page_not_found(e):
  '''custom 404'''
  # note that we set the 404 status explicitly
  return render_template('404.html'), 404

@app.route('/')
def index():
  '''home page'''
  form = AddCupcakeForm()
  return render_template('index.html', form=form)

# REST API

@app.route('/api/cupcakes')
def cakes_list():
  '''return JSON for all cupcakes'''
  all_cupcakes = [cake.serialize() for cake in Cupcake.query.order_by(func.upper(Cupcake.flavor)).all()]
  return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cake(id):
  '''get cake by id'''
  cake = Cupcake.query.get_or_404(id)
  return jsonify(cupcake = cake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cake():
  '''create new cupcake'''
  # create cupcake from json input
  flavor = request.json['flavor']
  size = request.json['size']
  rating = request.json['rating']
  image = request.json['image']
  new_cake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)
  # add cupcake to database
  db.session.add(new_cake)
  db.session.commit()
  # create response json
  response_json = jsonify(cupcake = new_cake.serialize())
  return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cake(id):
  '''update cake by id'''
  cake = Cupcake.query.get_or_404(id)

  cake.flavor = request.json.get('flavor', cake.flavor)
  cake.size = request.json.get('size', cake.size)
  cake.rating = request.json.get('rating', cake.rating)
  cake.image = request.json.get('image', cake.image)

  db.session.add(cake)
  db.session.commit()
  return jsonify(cupcake = cake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cake(id):
  '''delete cake by id'''
  cake = Cupcake.query.get_or_404(id)
  db.session.delete(cake)
  db.session.commit()
  return jsonify(message = 'cake has been deleted')

@app.route('/api/cupcakes/search')
def search_cakes():
  '''filter cakes by search'''
  search = request.args.get('search')
  # check to see if input is numeric
  if search.isnumeric():
    # convert string to int
    int(search)
    # filter by search integer value
    byRating = Cupcake.rating == search
    filtered_cupcakes = [cake.serialize() for cake in Cupcake.query.filter(byRating).all()]
  else:
    # filter by search string value
    byFlavor = Cupcake.flavor.ilike(f'%{search}%')
    bySize = Cupcake.size.ilike(f'%{search}%')
    filtered_cupcakes = [cake.serialize() for cake in Cupcake.query.filter(byFlavor | bySize).order_by(func.lower(Cupcake.flavor)).all()]
  # return results list
  return jsonify(cupcakes=filtered_cupcakes)