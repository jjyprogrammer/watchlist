from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click
from datetime import timedelta


app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = 'dev'


db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop', is_flag = True, help = 'Create after drop!')

def initdb(drop):
    """initialize """
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("initialize database")

@app.cli.command()
def	forge():
    """Generate	fake	data."""
    db.create_all()
    #	全局的两个变量移动到这个函数内
    name	=	'Grey	Li'
    movies	=	[
        {'title':	'My	Neighbor	Totoro',	'year':	'1988'},
        {'title':	'Dead	Poets	Society',	'year':	'1989'},
        {'title':	'A	Perfect	World',	'year':	'1993'},
        {'title':	'Leon',	'year':	'1994'},
        {'title':	'Mahjong',	'year':	'1996'},
        {'title':	'Swallowtail	Butterfly',	'year':	'1996'},
        {'title':	'King	of	Comedy',	'year':	'1999'},
        {'title':	'Devils	on	the	Doorstep',	'year':	'1999'},
        {'title':	'WALL-E',	'year':	'2008'},
        {'title':	'The	Pork	of	Music',	'year':	'2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for	m	in	movies:
        movie	=	Movie(title=m['title'],	year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60 :
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie = Movie(title = title, year = year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user = user)

@app.route('/movie/edit/<int:movie_id>',	methods=['GET',	'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input!')
            return redirect(url_for('edit', movie_id = movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html', movie = movie)

@app.route('/movie/delete/<int:movie_id>', methods = ['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))