"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory, sessions
from app.models import Property
from app.form import PropertyForm
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

"""routes to implement 
1/ /properties/create : form to add new house
2. /properties  : list all propeties in the database
3. /properties/<propertyid>   : viewing individual property"""

@app.route('/property/create', methods =['Post']) #route to create form
def create(): #view function to the create property form
    form = PropertyForm()

    if request.method =='POST':
        if form.validate_on_submit():
            propertytitle = form.propertytitle.data
            description = form.description.data
            rooms = form.rooms.data
            bathrooms =form.bathrooms.data
            price = form.price.data
            proptype = form.proptype.data
            location = form.location.data
            photo = form.photo.data
            filename= secure_filename(photo.filename)
            newlisting= Property(propertytitle, description, rooms, bathrooms, price, proptype,location, filename)
            db.session.add(newlisting)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('This property has been successfully saved','Success')
            return redirect(url_for('allproperties.html'))
    return render_template('addprop.html', form=form)

def get_uploaded_image():
    uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'])
    uploaded_images = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    return uploaded_images

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
