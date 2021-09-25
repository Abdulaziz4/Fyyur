#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask, render_template, request,
                   Response, flash, redirect, url_for, jsonify)
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import ShowForm, VenueForm, ArtistForm
import datetime
from models import (Venue, Artist, Show, current_datetime, db, setup_db)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

setup_db(app)

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')  # Completed
def venues():
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # Get cities and states distictly
    cities_states = Venue.query.distinct(Venue.city, Venue.state)

    data = []
    # iterate over the list
    for cs in cities_states:
        # Get the list of venues that have the same cities and venues
        venues_list = Venue.query.filter_by(
            city=cs.city).filter_by(state=cs.state)

        filtered_data = []

        for venue in venues_list:
            filtered_data.append(venue.preview_format())

        data.append({
            "city": cs.city,
            "state": cs.state,
            "venues": filtered_data,
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])  # Completed
def search_venues():
    search_term = request.form.get('search_term', '')

    search_res = Venue.query.filter(
        Venue.name.ilike('%' + search_term + '%'))

    count = 0
    for venue in search_res:
        count += 1

    response = {
        "count": count,
        "data": [],
    }

    for venue in search_res:
        response["data"].append(venue.preview_format())

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')  # Completed
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)

    data = venue.details_format()

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])  # Completed
def create_venue_submission():

    try:
        form = VenueForm(request.form)

        venue = Venue()
        form.populate_obj(venue)

        venue.insert()
    # on successful db insert, flash success
        flash('Venue ' + request.form['name'] +
              ' was successfully listed!')

    except Exception as e:
        print(e)
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form["name"] + ' could not be listed.')

    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])  # Completed
def delete_venue(venue_id):

    try:
        venue = Venue.query.get(venue_id)
        venue.delete()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')  # Completed
def artists():
    all_artists = Artist.query.order_by("id").all()

    data = []
    for artist in all_artists:
        data.append(artist.preview_format())

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])  # Completed
def search_artists():

    search_term = request.form.get('search_term', '')

    search_res = Artist.query.filter(
        Artist.name.ilike('%' + search_term + '%'))

    count = 0
    for artist in search_res:
        count += 1

    response = {
        "count": count,
        "data": [],
    }

    for artist in search_res:
        response["data"].append(artist.preview_format())

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')  # Completed
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    artist = Artist.query.get(artist_id)
    data = artist.details_format()
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])  # Completed
def edit_artist(artist_id):

    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])  # Completed
def edit_artist_submission(artist_id):
  
    try:
        form = ArtistForm(request.form)
        artist = Artist.query.get(artist_id)

        form.populate_obj(artist)
        artist.update()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])  # Completed
def edit_venue(venue_id):

    venue = Venue.query.get(venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    form = VenueForm(obj=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])  # Completed
def edit_venue_submission(venue_id):

    try:

        form = VenueForm(request.form)
        venue = Venue.query.get(venue_id)
        form.populate_obj(venue)
        venue.update()
    except Exception as e:
        print(e)
        db.session.rollback()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])  # Completed
def create_artist_submission():
    # called upon submitting the new artist listing form
    try:
        form = ArtistForm(request.form)
        artist = Artist()

        form.populate_obj(artist)
        artist.insert()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')  # Completed
def shows():
    # displays list of shows at /shows
    
    all_shows = Show.query.all()
    data = []

    for show in all_shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
        })

    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. 
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])  # Completed
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
  
    try:

        form = ShowForm(request.form)
        artist_id = form.artist_id.data
        venue_id = form.venue_id.data

        unvaild_id = Artist.query.filter_by(id=artist_id).first(
        ) is None or Venue.query.filter_by(id=venue_id).first() is None

        if unvaild_id:
            raise Exception("Artist/Venue doesn't exist")

        show = Show(artist_id=artist_id,
                    venue_id=venue_id,
                    start_time=form.start_time.data,
                    )

        show.insert()

    # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
     # on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
