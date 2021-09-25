from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_moment import Moment


db = SQLAlchemy()
current_datetime = datetime.datetime.now().isoformat()


def setup_db(app):
    moment = Moment(app)
    app.config.from_object('config')
    db.init_app(app)
    Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(
        db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="venue")

    def upcoming_shows(self):
        return Show.query.join(Venue, Show.venue_id == self.id).filter(Show.start_time >= current_datetime)

    def past_shows(self):
        return Show.query.join(Venue, Show.venue_id == self.id).filter(Show.start_time < current_datetime)

    def format_shows(self, shows_query):
        shows = []
        for show in shows_query:
            shows.append(show.artist_format())
        return shows

    def preview_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "num_upcoming_shows": len(self.format_shows(self.upcoming_shows())),
        }

    def details_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website_link,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows": self.format_shows(self.past_shows()),
            "upcoming_shows": self.format_shows(self.upcoming_shows()),
            "past_shows_count": len(self.format_shows(self.past_shows())),
            "upcoming_shows_count": len(self.format_shows(self.upcoming_shows())),
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(
        db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artist")

    def upcoming_shows(self):
        return Show.query.join(Artist, Show.artist_id == self.id).filter(Show.start_time >= current_datetime)

    def past_shows(self):
        return Show.query.join(Artist, Show.artist_id == self.id).filter(Show.start_time < current_datetime)

    def format_shows(self, shows_query):
        shows = []
        for show in shows_query:
            shows.append(show.venue_format())
        return shows

    def preview_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "num_upcoming_shows": len(self.format_shows(self.upcoming_shows())),
        }

    def details_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "seeking_venue": self.seeking_venue,
            "image_link": self.image_link,
            "seeking_description": self.seeking_description,
            "past_shows": self.format_shows(self.past_shows()),
            "upcoming_shows": self.format_shows(self.upcoming_shows()),
            "past_shows_count": len(self.format_shows(self.past_shows())),
            "upcoming_shows_count": len(self.format_shows(self.upcoming_shows())),
            "website": self.website_link,
            "facebook_link": self.facebook_link,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"))

    def artist_format(self):
        return {
            "artist_id": self.artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": self.start_time,
        }

    def venue_format(self):
        return {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "start_time": self.start_time,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
