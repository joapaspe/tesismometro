from flask import Flask
import jinja2
import webapp2
import os
from initialize_bd import initialize_bd
from flask import render_template
import tesis_bd
from flask import request

app = Flask(__name__)


# users = ["Pastor", "Flores", "Escamilla"]
#
#
# for user in users:
#     dr = tesis_bd.Doctor(name=user)
#     dr.put()

@app.route('/test')
def hello_world():
    results = [
        {
            'name': 'Flores',
            'words': 20000,
            'figures': 100,
            'equations_inline': 500,
            'equations': 50,
            'last_date': "today"
        },
    {
            'name': 'Escamilla',
            'words': 20000,
            'figures': 100,
            'equations': 50,
            'equations_inline': 500,
            'last_date': "today"
        },
    {
            'name': 'Pastor',
            'words': 20000,
            'figures': 100,
            'equations': 50,
            'equations_inline': 500,
            'last_date': "today",
        },

    ]

    return render_template('index.html', results=results)

@app.route('/')
def show_results():

    users = tesis_bd.Doctor.query().fetch()

    results = []

    for doctor in users:
        last_record = tesis_bd.LastRecord.query(tesis_bd.LastRecord.doctor == doctor.key).fetch()
        if last_record:
            last_record = last_record[0]
            record = last_record.record.get()
            res = {
                'name': doctor.name,
                'words': record.words,
                'figures': record.figures,
                'equations': record.equations,
                'equations_inline': record.equations_inline,
                'date': record.date
            }
            results.append(res)

        results.sort(key=lambda x:-x["words"])

    return render_template('index.html', results=results)

# @app.route('/clear')
# def reset_bd():
#     initialize_bd()
#     return show_results()

@app.route('/post', methods=['GET', 'POST'])
def post_record():

    if request.method != 'POST':
        return
    params = request.form
    # Buscar el usuari
    doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name == params["name"]).fetch()
    if not doctor:
        return
    doctor = doctor[0]
    # Crear el record


    lrecords = tesis_bd.LastRecord.query(tesis_bd.LastRecord.doctor == doctor.key).fetch()
    if not lrecords:
        # Create an empty record
        empty_record = tesis_bd.Record(doctor.key, 0, 0, 0, 0)
        empty_record.put()
        lrecord = tesis_bd.LastRecord(doctor=doctor.key, record=empty_record.key)
        lrecord.put()
    else:
        lrecord= lrecords[0]


    # Si es el mateix dia actualizem
    import datetime
    now = datetime.datetime.now()
    day, month, year = now.day, now.month, now.year

    equations = int(params["equations"])
    words = int(params["words"])
    equations_inline = int(params["equations_inline"])
    figures = int(params["figures"])

    record = lrecord.record.get()
    if record.date.day == day and\
       record.date.month == month and\
       record.date.year == year:
            record.equations = equations
            record.words= words
            record.equations_inline = equations_inline
            record.figures = figures
            record.put()
    else:
        record = tesis_bd.Record(doctor=doctor.key, words=words, equations=equations, equations_inline=equations_inline, figures=figures)
        record.put()
        lrecord.record = record.key
        lrecord.put()


    return render_template('show_post.html', doctor=params)
if __name__ == '__main__':
    app.run()

