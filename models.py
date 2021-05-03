from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode

db = SQLAlchemy()


class Artist(db.Model):
    id = db.Column(db.String(64), primary_key=True, nullable=True)
    name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    albums = db.relationship('Album', backref='b_artist', lazy=True)
    tracks = db.Column(db.String(128), nullable=True)
    self = db.Column(db.String(128), nullable=True)
        
    @property
    def self(self):
        return url_for("get_artist", id=self.id) 

    @property
    def tracks(self):
        return url_for("get_artist_tracks", id=self.id)
    
    @property
    def albums(self):
        return url_for("get_artist_albums", id=self.id)



class Album(db.Model):
    id = db.Column(db.String(64), primary_key=True, nullable=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('artist.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    artist = db.Column(db.String(128), nullable=True)
    tracks = db.relationship('Track', backref='b_album', lazy=True)
    self = db.Column(db.String(128), nullable=True)

    @property
    def self(self):
        return url_for("get_album", id=self.id) 
    
    @property
    def artist(self):
        return url_for("get_artist", id=self.artist_id) 

    @property
    def tracks(self):
        return url_for("get_album_tracks", id=self.id) 



class Track(db.Model):
    id = db.Column(db.String(64), primary_key=True, nullable=True)
    album_id = db.Column(db.String(64), db.ForeignKey('album.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    times_played = db.Column(db.Integer, default=0 , nullable=True)
    artist = db.Column(db.String(128), nullable=True)   #Acá se hace relación con ForeignKey??? ---------
    album = db.Column(db.String(128), nullable=True)
    self = db.Column(db.String(128), nullable=True)

    @property
    def self(self):
        return url_for("get_track", id=self.id) 
    
    @property
    def artist(self):
        album = Album.query.get_or_404(self.album_id)
        id_artista_buscado = album.artist_id
        return url_for("get_artist", id=id_artista_buscado) 

    @property
    def album(self):
        return url_for("get_album", id=self.album_id) 


'''class Puppy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128), nullable=False)

    @property
    def url(self):
        return url_for("get_puppy", id=self.id)   
'''