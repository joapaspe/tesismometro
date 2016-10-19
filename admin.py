"""Handles the http requests and interacts with the database"""
import os
from flask import Flask
import jinja2
from flask import render_template, redirect
import initialize_bd
import tesis_bd
from flask import request


# jinja2 configuration.
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

app = Flask(__name__)


@app.route('/admin/', methods=['GET'])
def admin_view():
    """
        User interface (only shows the token).
        :return: An http response with the submitted information.
    """

    # Check if the database is empty
    doctors = tesis_bd.Doctor.query().fetch()
    is_empty = False
    if len(doctors) == 0:
        is_empty = True

    template_dict = {
        'bd_is_empty': is_empty,
        'doctors': doctors
    }
    return render_template('admin.html', **template_dict)


@app.route('/admin/dummy/', methods=['GET'])
def create_dummy_database():
    """
        Creates dummy database (only for testing)
    """
    # Check if the database is empty
    doctors = tesis_bd.Doctor.query().fetch()
    if len(doctors) > 0:
        return render_template(
            'error.html', "The database must be empty in order to create dummy data")

    initialize_bd.initialize_bd()

    return redirect("/admin/")


@app.route('/admin/adduser/', methods=['POST'])
def add_user():
    name = request.form.get('name', '')
    email = request.form.get('email', '')

    if not name or not email:
        return render_template(
            'error.html', 'You must provide an email and name in order to create a new user.')

    if not initialize_bd.add_user(name, email):
        return render_template(
            'error.html', 'The user cannot be created.')

    return redirect('/admin/')


if __name__ == '__main__':
    app.run()
