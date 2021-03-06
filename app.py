from flask import Flask, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import json
import requests
from imdb import IMDb, IMDbError
from forms import ContactForm
from flask_mail import Mail, Message
from config import *


app = Flask(__name__)
app.secret_key = 'secretKey'


PIC_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PIC_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 25
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = SEND_MAIL
app.config['MAIL_PASSWORD'] = PASSWORD_MAIL
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
@app.route('/home')
def home():  # put application's code here
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image.JPG')
    return render_template('home.html', img_file=filename)


@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')


@app.route('/currentprojects')
def currentprojects():
    return render_template('currentproject.html')


@app.route('/music')
def music():
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.user_playlist_tracks(SPOTIFY_NAME, PLAYLIST_URI)
    tracks = results['items']

    return render_template('music.html', tracks=tracks)


@app.route('/books')
def books():
    response = requests.get(
        'https://www.googleapis.com/books/v1/users/115945058972361383352/bookshelves/1001/volumes?key='+API_KEY_BOOKS)
    data = json.loads(response.text)
    return render_template('books.html', response=data)




@app.route('/maps')
def show_maps():
    return render_template('map.html')


@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    form = ContactForm()
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        subject = request.form['subject']
        send_mail(subject=subject, message=message)
        return render_template('thankyou.html')
    else:
        return render_template('contactme.html', form=form)



@app.route('/')
def send_mail(subject, message):
    msg = Message(subject, sender=SEND_MAIL, recipients=[REC_MAIL])
    msg.body = message
    mail.send(msg)
    return 'Sent'

@app.route('/firstproject')
def showfirstproject():
    return render_template('projectjava.html')

@app.route('/movies')
def movies():
    try:
        movie_titles = { 'No Country for old man', 'Batman The Dark Knight',
                         'The big short', 'The wolf of Wallstreet',
                        'Dunkirk'}
        ia = IMDb()
        movies = []
        for m in movie_titles:
            movie = ia.search_movie(m)
            movies.append(movie[0])
        return render_template('movies.html', movies=movies, ia=ia)

    except TypeError as e:
        print()



@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404


@app.errorhandler(400)
def not_found_error(error):
    return render_template('error.html'), 400


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500


if __name__ == '__main__':
    app.run()
