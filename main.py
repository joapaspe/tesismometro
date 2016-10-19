"""Handles the http requests and interacts with the database"""
import os
import random
import json

from flask import Flask
import jinja2
import stats
from flask import render_template, redirect
import tesis_bd
from flask import request

from google.appengine.api import users

# jinja2 configuration.
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

app = Flask(__name__)


@app.route('/')
def show_results():
    """
        Main page.

        :return: The request with the rendered template.
    """
    doctors = tesis_bd.Doctor.query().fetch()
    results = []
    for doctor in doctors:
        last_record = tesis_bd.LastRecord.query(tesis_bd.LastRecord.doctor == doctor.key).fetch()
        if last_record:
            last_record = last_record[0]
            record = last_record.record.get()
            res = {
                'name': doctor.name
            }
            for field in tesis_bd.RECORD_FIELDS:
                res[field] = getattr(record, field)
            results.append(res)
        results.sort(key=lambda x: -x["words"])

    # Select the default drawing field.
    draw_field = request.args.get('draw')
    if not draw_field or draw_field not in tesis_bd.RECORD_FIELDS[:-1]:
        draw_field = 'words'
    draw_data = stats.get_draw_info(draw_field)

    # Compute the draw standings.
    week_standings = stats.get_week_standings()
    return render_template('index.html',
                           results=results,
                           headers=tesis_bd.RECORD_NAMES,
                           fields=tesis_bd.RECORD_FIELDS,
                           draw_data=json.dumps(draw_data),
                           week_standings=week_standings,
                           draw_field=tesis_bd.record_field_to_name[draw_field]
                          )


@app.route('/hist/<username>/')
def show_hist(username):
    """Extracts the histograms and show them to the final user.

    :param username: Doctor name to show stats about.
    :return: Rendered template with the doctor data stats.
    """
    draw_field = request.args.get('draw')

    doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name == username).fetch()
    if not doctor:
        return render_template('hist.html')

    doctor = doctor[0]
    records = tesis_bd.Record.query(
        tesis_bd.Record.doctor == doctor.key).order(-tesis_bd.Record.date).fetch()

    # Compute the difference with the previous record.
    diffs = []
    for i, record in enumerate(records):
        record_diff = {}
        for field in tesis_bd.RECORD_FIELDS[:-1]:
            if i == len(records) - 1:
                record_diff[field] = 0
            else:
                act = getattr(record, field)
                ant = getattr(records[i + 1], field)

                record_diff[field] = act - ant
        diffs.append(record_diff)

    # Default graph field.
    if not draw_field or draw_field not in tesis_bd.RECORD_FIELDS[:-1]:
        draw_field = 'words'

    draw_dates = [x.date.strftime('%Y-%m-%d') for x in records]
    return render_template('hist.html', records=records, doctor=doctor.name, difs=diffs,
                           fields=tesis_bd.RECORD_FIELDS[:-1], headers=tesis_bd.RECORD_NAMES,
                           draw_dates=draw_dates, draw_field=draw_field)


@app.route('/post', methods=['GET', 'POST'])
def post_record():
    """
            Request for adding the data to the database.

            :return: An http response with the submitted information
    """
    if request.method != 'POST':
        return render_template(
            "error.html", message="GET mode not allowed for adding a new record.")

    params = request.form
    doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name == params["name"]).fetch()
    if not doctor:
        return render_template("error.html", message="The doctor is not found.")
    doctor = doctor[0]

    # Check the token.
    if "token" not in params or doctor.token != params["token"]:
        return render_template("error.html", message="Unable to authenticate the doctor.")

    # Get the record tu update.
    record_list = tesis_bd.LastRecord.query(tesis_bd.LastRecord.doctor == doctor.key).fetch()
    if not record_list:
        # Create an empty record
        empty_record = tesis_bd.Record(doctor=doctor.key)
        empty_record.put()
        last_record = tesis_bd.LastRecord(doctor=doctor.key, record=empty_record.key)
        last_record.put()
    else:
        last_record = record_list[0]

    # If the record is from the same day we update it.
    import datetime
    now = datetime.datetime.now()
    day, month, year = now.day, now.month, now.year

    equations = int(params["equations"])
    words = int(params["words"])
    equations_inline = int(params["equations_inline"])
    figures = int(params["figures"])
    cites = int(params["cites"])
    pages = int(params["pages"])
    record = last_record.record.get()
    last_values = [getattr(record, field) for field in tesis_bd.RECORD_FIELDS[:-1]]

    if record.date.day == day and record.date.month == month and record.date.year == year:
        record.equations = equations
        record.words = words
        record.equations_inline = equations_inline
        record.figures = figures
        record.pages = pages
        record.cites = cites
        record.date = datetime.datetime.now() + datetime.timedelta(hours=1)
        record.put()
    else:
        record = tesis_bd.Record(doctor=doctor.key, words=words,
                                 equations=equations, equations_inline=equations_inline,
                                 figures=figures, cites=cites, pages=pages,
                                 date=datetime.datetime.now()+datetime.timedelta(hours=1))
        record.put()
        last_record.record = record.key
        last_record.put()

    diff_values = [getattr(record, field) - last_values[i]
                   for i, field in enumerate(tesis_bd.RECORD_FIELDS[:-1])]
    diff_values.append(record.date.strftime('%Y-%m-%d %H:%M'))
    stats.update_data()
    return render_template('show_post.html', doctor=diff_values, fields=tesis_bd.RECORD_FIELDS)


@app.route('/user', methods=['GET'])
def user_view():
    """
        User interface (only shows the token).
        :return: An http response with the submitted information.
    """
    user = users.get_current_user()

    if not user:
        return redirect(users.create_login_url("/user"))
    email = user.email()
    doctors = tesis_bd.Doctor.query(tesis_bd.Doctor.email == email).fetch()

    if len(doctors) == 0:
        return render_template('error.html', message="User not found in the DB.")

    doctor = doctors[0]
    name = doctor.name

    if not doctor.token:
        doctor.token = "%016x" % random.getrandbits(64)
    code = doctor.token

    doctor.put()
    logout_url = users.create_logout_url("/")
    return render_template('user_view.html', login=doctor.name, name=name, email=email, code=code,
                           logout_url=logout_url)


if __name__ == '__main__':
    app.run()
