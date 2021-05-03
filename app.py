import sys
from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from models import db, Artist, Album, Track
from schemas import ma, artist_schema, artists_schema, album_schema, albums_schema, track_schema, tracks_schema
from slugify import slugify
from base64 import b64encode

from decouple import config as config_decouple


#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///artist.db"
#db.init_app(app)
#ma.init_app(app)

def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        db.create_all()

    return app

enviroment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(enviroment)



#------------------------------------------------------------------------------
# GET METHOD
#------------------------------------------------------------------------------

#GET Artists 
@app.route("/artists", methods=["GET"])
def list_artists():
    all_artists = Artist.query.all()
    return artists_schema.jsonify(all_artists)


#GET Artist by ID
@app.route("/artists/<id>", methods=["GET"])
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    return artist_schema.jsonify(artist)


#GET Artist Albums 
@app.route("/artists/<id>/albums", methods=["GET"])
def get_artist_albums(id):
    all_albums = Album.query.all()
    albums_artista = []
    for i in all_albums:
        if i.artist_id == id:
            albums_artista.append(i)
    return albums_schema.jsonify(albums_artista)


#GET Artist Tracks 
@app.route("/artists/<id>/tracks", methods=["GET"])
def get_artist_tracks(id):
    all_albums = Album.query.all()
    albums_artista = []
    tracks_artista = []
    for i in all_albums:
        if i.artist_id == id:
            albums_artista.append(i.id)
    all_tracks = Track.query.all()
    for j in all_tracks:
        if j.album_id in albums_artista:
            tracks_artista.append(j)
    return tracks_schema.jsonify(tracks_artista)


#GET Albums
@app.route("/albums", methods=["GET"])
def list_albums():
    all_albums = Album.query.all()
    return albums_schema.jsonify(all_albums)


#GET Album by ID
@app.route("/albums/<id>", methods=["GET"])
def get_album(id):
    album = Album.query.get_or_404(id)
    return album_schema.jsonify(album)


#GET Album Tracks
@app.route("/albums/<id>/tracks", methods=["GET"])
def get_album_tracks(id):
    all_tracks = Track.query.all()
    tracks_album = []
    for i in all_tracks:
        if i.album_id == id:
            tracks_album.append(i)
    return tracks_schema.jsonify(tracks_album)


#GET Tracks
@app.route("/tracks", methods=["GET"])
def list_tracks():
    all_tracks = Track.query.all()
    return tracks_schema.jsonify(all_tracks)


#GET Track by ID
@app.route("/tracks/<id>", methods=["GET"])
def get_track(id):
    track = Track.query.get_or_404(id)
    return track_schema.jsonify(track)


#------------------------------------------------------------------------------
# POST METHOD
#------------------------------------------------------------------------------

#POST Artista
@app.route("/artists", methods=["POST"])
def create_artist():
    try:
        nombre_codif = b64encode(request.json['name'].encode()).decode('utf-8')
        nombre_corto = nombre_codif[:22]
        request.json['id'] = nombre_corto
        artist = artist_schema.load(request.json, session=db.session)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    db.session.add(artist)
    db.session.commit()

    resp = jsonify({"message": "created"})
    resp.status_code = 201
    #resp.headers["Location"] = puppy.url
    return resp


#POST Album
@app.route("/artists/<id>/albums", methods=["POST"])
def create_album(id):
    try:
        nombre_a_codificar = request.json['name'] + ":" + id
        nombre_codif = b64encode(nombre_a_codificar.encode()).decode('utf-8')
        nombre_corto = nombre_codif[:22]
        request.json['artist_id'] = id
        request.json['id'] = nombre_corto
        album = album_schema.load(request.json, session=db.session)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    db.session.add(album)
    db.session.commit()

    resp = jsonify({"message": "created"})
    resp.status_code = 201
    #resp.headers["Location"] = puppy.url
    return resp


#POST Track
@app.route("/albums/<id>/tracks", methods=["POST"])
def create_track(id):
    try:
        nombre_a_codificar = request.json['name'] + ":" + id
        nombre_codif = b64encode(nombre_a_codificar.encode()).decode('utf-8')
        nombre_corto = nombre_codif[:22]
        request.json['album_id'] = id
        request.json['id'] = nombre_corto
        track = track_schema.load(request.json, session=db.session)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    db.session.add(track)
    db.session.commit()

    resp = jsonify({"message": "created"})
    resp.status_code = 201
    #resp.headers["Location"] = puppy.url
    return resp



#------------------------------------------------------------------------------
# DELETE METHOD
#------------------------------------------------------------------------------

#DELETE Artist
@app.route("/artists/<id>", methods=["DELETE"])
def delete_artist(id):
    artist = Artist.query.get_or_404(id)
    db.session.delete(artist)
    db.session.commit()
    return jsonify({"message": "deleted"})


#DELETE Album
@app.route("/albums/<id>", methods=["DELETE"])
def delete_album(id):
    album = Album.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    return jsonify({"message": "deleted"})


#DELETE Track
@app.route("/tracks/<id>", methods=["DELETE"])
def delete_track(id):
    track = Track.query.get_or_404(id)
    db.session.delete(track)
    db.session.commit()
    return jsonify({"message": "deleted"})



#------------------------------------------------------------------------------
# PUT METHOD
#------------------------------------------------------------------------------

#PUT Reproducir todas las canciones de un artista
'''
@app.route("/puppies/<id>", methods=["PUT"])
def edit_canciones_artista(id):
    artista = Artist.query.get_or_404(id)
    try:
        artista = artist_schema.load(request.json, instance=artista)   #(request.json, session=db.session)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    all_albums = Album.query.all()
    albums_artista = []
    tracks_artista = []
    for i in all_albums:
        if i.artist_id == id:
            albums_artista.append(i.id)
    all_tracks = Track.query.all()
    for j in all_tracks:
        if j.album_id in albums_artista:
            j.times_played += 1
    
    db.session.add(puppy)
    db.session.commit()

    resp = jsonify({"message": "updated"})
    return resp
'''



'''
@app.route("/puppies/<int:id>")
def get_puppy(id):
    puppy = Puppy.query.get_or_404(id)
    return puppy_schema.jsonify(puppy)


@app.route("/puppies/", methods=["GET"])
def list_puppies():
    all_puppies = Puppy.query.all()
    return puppies_schema.jsonify(all_puppies)


@app.route("/puppies/", methods=["POST"])
def create_puppy():
    try:
        puppy = puppy_schema.load(request.form)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    puppy.slug = slugify(puppy.name)
    db.session.add(puppy)
    db.session.commit()

    resp = jsonify({"message": "created"})
    resp.status_code = 201
    resp.headers["Location"] = puppy.url
    return resp


@app.route("/puppies/<int:id>", methods=["POST"])
def edit_puppy(id):
    puppy = Puppy.query.get_or_404(id)
    try:
        puppy = puppy_schema.load(request.form, instance=puppy)
    except ValidationError as errors:
        resp = jsonify(errors.messages)
        resp.status_code = 400
        return resp

    puppy.slug = slugify(puppy.name)
    db.session.add(puppy)
    db.session.commit()

    resp = jsonify({"message": "updated"})
    return resp


@app.route("/puppies/<int:id>", methods=["DELETE"])
def delete_puppy(id):
    puppy = Puppy.query.get_or_404(id)
    db.session.delete(puppy)
    db.session.commit()
    return jsonify({"message": "deleted"})
'''

@app.errorhandler(404)
def page_not_found(error):
    resp = jsonify({"error": "not found"})
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            db.create_all()
        print("Database created!")

    elif "seeddb" in sys.argv:
        with app.app_context():
            a1 = Artist(id = "TWljaGFlbCBKYWNrc29u",
                        name = "Michael Jackson",
                        age = 21)
            db.session.add(a1)

            al1 = Album(id = "T2ZmIHRoZSBXYWxsOlRXbG",
                        artist_id = "TWljaGFlbCBKYWNrc29u",
                        name = "Off the Wall",
                        genre = "Pop")

            db.session.add(al1)
            
            t1 = Track(id = "RG9uJ3QgU3RvcCAnVGlsIF",
                       album_id = "T2ZmIHRoZSBXYWxsOlRXbG",
                       name = "Don't Stop 'Til You Get Enough",
                       duration = 4.1,
                       times_played = 0)

            db.session.add(t1)

            db.session.commit()
        print("Database seeded!")

    else:
        app.run(debug=True)