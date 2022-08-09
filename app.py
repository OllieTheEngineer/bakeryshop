"""Flask app for Cupcakes"""
from flask import Flask, render_template, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/api/cupcakes")
def all_cupcakes():
    cupcakes = Cupcake.query.all()
    return render_template("cupcakes.html", cupcakes=cupcakes)

@app.route("/api/cupcakes/<ini:cupcake_id>")
def spec_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return render_template('speciality.html', )

@app.route("/api/cupcakes", methods=['POST'])
def new_cupcake():

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image' or None])
    
    db.session.add(cupcake)
    db.session.commit()

    return render_template("create.html", cupcake=cupcake)

@app.route("/api/cupcakes/<ini:cupcake_id>", methods=["PATCH"])
def edit_cupcake(cupcake_id):

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return