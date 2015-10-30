__author__ = 'jpastor'
import tesis_bd
import  datetime
records_data = {}
last_update = datetime.datetime(2015,1,1)

def update_data():
    global last_update
    records = tesis_bd.Record.query().fetch()
    users = tesis_bd.Doctor.query().fetch()

    key_to_doctor = {}
    for user in users:
        key_to_doctor[user.key] = user.name
        records_data[user.name] = []

    for record in records:
        name = key_to_doctor[record.doctor]
        values = (record.date.strftime('%Y-%m-%d %H:%M'), record.words)
        records_data[name].append(values)

    last_update = datetime.datetime.today()

def needs_update():
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if last_update < now:
        return True
    return False

def get_draw_words():
    if needs_update():
        update_data()
    return records_data
