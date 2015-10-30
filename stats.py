__author__ = 'jpastor'
import tesis_bd
import  datetime
records_data = {}
week_standings = []
last_update = datetime.datetime(2015, 1, 1)

def update_data():
    global last_update
    records = tesis_bd.Record.query().fetch()
    users = tesis_bd.Doctor.query().fetch()

    key_to_doctor = {}

    last_week_record = {}
    recent_week_record = {}

    for user in users:
        key_to_doctor[user.key] = user.name
        records_data[user.name] = []
        last_week_record[user.name] = None
        recent_week_record[user.name] = None

    last_week = (datetime.datetime.today() - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    for record in records:
        name = key_to_doctor[record.doctor]
        values = (record.date.strftime('%Y-%m-%d %H:%M'), record.words)
        records_data[name].append(values)

        if record.date > last_week and\
            (not last_week_record[name] or record.date < last_week_record[name].date):
            last_week_record[name] = record

        if not recent_week_record[name] or record.date > recent_week_record[name].date:
            recent_week_record[name] = record

    week_standings[:] = []
    for user in users:
        name = user.name
        week_words = 0

        if last_week_record[name] and recent_week_record[name]:
            week_words = recent_week_record[name].words - last_week_record[name].words
        week_standings.append((name, week_words))

    week_standings.sort(key=lambda x:-x[1])
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

def get_week_standings():
    if needs_update():
        update_data()
    # Convert to sorted list
    return week_standings
