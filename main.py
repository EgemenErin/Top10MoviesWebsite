from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

def get_db_connection():
    connection = sqlite3.connect("instances/top10movies.db", timeout=10)
    connection.row_factory = sqlite3.Row
    return connection

with get_db_connection() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title VARCHAR(250) NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            description VARCHAR(250),
            rating FLOAT NOT NULL,
            ranking INTEGER NOT NULL,
            review VARCHAR(250),
            img_url VARCHAR(250) NOT NULL
        )
    """)
    db.commit()

class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")
@app.route("/")
def home():
    with get_db_connection() as db:
        movies = db.execute("SELECT * FROM movies").fetchall()
    return render_template("index.html", movies=movies)
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = RateMovieForm()
    with get_db_connection() as db:
        movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
        form.rating.data = movie["rating"]
        form.review.data = movie["review"]
        if form.validate_on_submit():
            new_rating = form.rating.data
            new_review = form.review.data
            db.execute("""
                UPDATE movies
                SET rating = ?, review = ?
                WHERE id = ?
            """, (new_rating, new_review, movie_id))
            db.commit()
            return redirect(url_for('home'))

    return render_template("edit.html", form=form, movie=movie)




if __name__ == '__main__':
    app.run(debug=True)
