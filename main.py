from flask import Flask
from initialize_bd import initialize_bd, hotfix
import os
import jinja2
import stats
from flask import render_template
import tesis_bd
from flask import request
import json
# jinja2 stuff

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)

app = Flask(__name__)
# users = ["Pastor", "Flores", "Escamilla"]
#
#
# for user in users:
#     dr = tesis_bd.Doctor(name=user)
#     dr.put()


# Filters

@app.route('/')
def show_results():

    draw_field = request.args.get('draw')

    if not draw_field or draw_field not in tesis_bd.record_fields[:-1]:
        draw_field = 'words'

    users = tesis_bd.Doctor.query().fetch()

    results = []

    for doctor in users:
        last_record = tesis_bd.LastRecord.query(tesis_bd.LastRecord.doctor == doctor.key).fetch()
        if last_record:
            last_record = last_record[0]
            record = last_record.record.get()

            res = {
                'name': doctor.name
            }
            for field in tesis_bd.record_fields:
                res[field] = getattr(record, field)

            results.append(res)

        results.sort(key=lambda x:-x["words"])

    draw_data = stats.get_draw_info(draw_field)

    week_standings = stats.get_week_standings()
    return render_template('index.html',
                           results=results,
                           headers=tesis_bd.record_names,
                           fields=tesis_bd.record_fields,
                           draw_data=json.dumps(draw_data),
                           week_standings=week_standings,
                           draw_field = tesis_bd.record_field_to_name[draw_field],
                           )

@app.route('/hist/<username>/')
def show_hist(username):
    draw_field = request.args.get('draw')

    if not draw_field or draw_field not in tesis_bd.record_fields[:-1]:
        draw_field = 'words'
    # Buscar el usuari
    doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name == username).fetch()
    if not doctor:
        return render_template('hist.html')

    doctor = doctor[0]
    records = tesis_bd.Record.query(tesis_bd.Record.doctor == doctor.key).order(-tesis_bd.Record.date).fetch()


    difs = []

    for r, record in enumerate(records):
        record_dif = {}
        for field in tesis_bd.record_fields[:-1]:
            if r == len(records) - 1:
                record_dif[field] = 0
            else:
                act = getattr(record,field)
                ant = getattr(records[r+1],field)

                record_dif[field] = act - ant
        difs.append(record_dif)
    draw_dates = [x.date.strftime('%Y-%m-%d') for x in records]
    return render_template('hist.html', records=records, doctor=doctor.name, difs=difs, fields=tesis_bd.record_fields[:-1], headers=tesis_bd.record_names,
                           draw_dates = draw_dates, draw_field=draw_field)

#estas dos funciones implican peligro https://www.youtube.com/watch?v=8CYzxXWRt-k

# @app.route('/clear')
# def reset_bd():
#     initialize_bd()
#     return show_results()

# @app.route('/update')
# def UpdateSchema(cursor=None, num_updated=0):
#     records = tesis_bd.Record.query().fetch()
#
#     for record in records:
#         record.put()
#
#     return show_results()

@app.route('/hotfix')
def fix():
#    hotfix()
    return show_results()

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
        empty_record = tesis_bd.Record(doctor.key, 0, 0, 0, 0,0,0)
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
    cites = int(params["cites"])
    pages = int(params["pages"])

    record = lrecord.record.get()

    last_values = [getattr(record, field) for field in tesis_bd.record_fields[:-1]]

    if record.date.day == day and\
       record.date.month == month and\
       record.date.year == year:
            record.equations = equations
            record.words = words
            record.equations_inline = equations_inline
            record.figures = figures
            record.pages = pages
            record.cites = cites
            record.date = datetime.datetime.now()+datetime.timedelta(hours=1)
            record.put()
    else:
        record = tesis_bd.Record(doctor=doctor.key, words=words, equations=equations, equations_inline=equations_inline, figures=figures, cites=cites, pages=pages, date=datetime.datetime.now()+datetime.timedelta(hours=1))
        record.put()
        lrecord.record = record.key
        lrecord.put()

    diff_values = [getattr(record, field)-last_values[i] for i, field in enumerate(tesis_bd.record_fields[:-1])]
    diff_values.append(record.date.strftime('%Y-%m-%d %H:%M'))
    stats.update_data()
    return render_template('show_post.html', doctor=diff_values, fields=tesis_bd.record_fields)



if __name__ == '__main__':
    app.run()

