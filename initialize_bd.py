""" Creates a fake DB for dummy purposes"""
import datetime
import random
import tesis_bd
import stats

__author__ = 'joanpastor'


def clear_bd():
    """ Drop all the entities in the database."""
    # Remove data.
    doctors = tesis_bd.Doctor.query().fetch()
    records = tesis_bd.Record.query().fetch()
    last_records = tesis_bd.LastRecord.query().fetch()

    for doctor in doctors:
        doctor.key.delete()

    for record in records:
        record.key.delete()
    for record in last_records:
        record.key.delete()


def initialize_bd():
    """Resets the bd with the default users and empty data"""
    users = ['Alice', 'Bob', 'Chris']
    emails = ['alice@example.com', 'bob@example.com', 'chris@example.com']

    for i, user in enumerate(users):
        doctor = tesis_bd.Doctor(name=user, email=emails[i])
        doctor.put()
        # The record
        record = tesis_bd.Record(doctor=doctor.key, words=0, figures=0,
                                 equations=0, equations_inline=0)
        record.put()
        max_words = 30000
        num_days = 20
        for days in range(num_days):
            words = random.randint(1, max_words)
            figures = words/100
            equations = words/1000
            equations_inline = words/50
            date = datetime.datetime.now() - datetime.timedelta(days=num_days-days)
            new_record = tesis_bd.Record(doctor=doctor.key, words=words,
                                         figures=figures, equations=equations,
                                         equations_inline=equations_inline, date=date)
            new_record.put()

        # The last record.
        last_record = tesis_bd.LastRecord(doctor=doctor.key, record=record.key)
        last_record.put()
    # Refresh the stats.
    stats.update_data()


def add_user(name, email):
    """Adds a new user into the database.

    :param name: Name of the user.
    :param email: Email used for the Google ID.
    :return: The new entity created. None if it is not possible to create the user.
    """
    # Check if the use exists
    doctors = tesis_bd.Doctor.query(tesis_bd.Doctor.email == email).fetch()
    if len(doctors) > 0:
        # Cannot create the doctor.
        return None

    new_doctor = tesis_bd.Doctor(name=name, email=email)
    new_doctor.put()

    return new_doctor


