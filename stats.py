""" Functions to compute thesis stats."""
import datetime
import tesis_bd

__author__ = 'jpastor'

# TODO(joanpastor): Add this functionality in a singleton class.
records_data = {}
week_standings = []
last_update = datetime.datetime(2015, 1, 1)


def update_data():
    """ Reloads the information from the database."""
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

    last_week = (datetime.datetime.today() - datetime.timedelta(days=7))\
        .replace(hour=0, minute=0, second=0, microsecond=0)

    for record in records:
        # The record corresponds to a non-existing doctor.
        if record.doctor not in key_to_doctor:
            continue
        name = key_to_doctor[record.doctor]
        records_data[name].append(record)

        if record.date < last_week and\
            (not last_week_record[name] or record.date > last_week_record[name].date):
            last_week_record[name] = record

        if not recent_week_record[name] or record.date > recent_week_record[name].date:
            recent_week_record[name] = record

    week_standings[:] = []
    for user in users:
        name = user.name
        week_words = 0

        if last_week_record[name] and recent_week_record[name]:
            week_words = recent_week_record[name].words - last_week_record[name].words
        elif recent_week_record[name]:
            week_words = recent_week_record[name].words
        week_standings.append((name, week_words))

    week_standings.sort(key=lambda x: -x[1])
    last_update = datetime.datetime.today()


def needs_update():
    """ Checks if the day has change and the stats are recomputed"""
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if last_update < now:
        return True
    return False


def _extract_field(field='words'):
    field_data = {}
    for user in records_data:
        field_data[user] = [(x.date.strftime('%Y-%m-%d %H:%M'),
                             getattr(x, field)) for x in records_data[user]]
    return field_data


def get_draw_info(field='words'):
    """Extract all the fields by time from the list of records
        :returns: field_data structure with a list of tuples [(date, field_value)]
    """
    if needs_update():
        update_data()
    return _extract_field(field)


def get_week_standings():
    """ Return the precomputed week_standings"""
    if needs_update():
        update_data()
    # Convert to sorted list
    return week_standings
