""" Creates a fake DB for dummy purposes"""
import datetime
import random
import tesis_bd

__author__ = 'joanpastor'


def initialize_bd():
    """Resets the bd with the default users and empty data"""
    users = ['Pastor', 'Flores', 'Escamilla']
    emails = ['joapaspe@gmail.com', 'enflosae@gmail.com', 'joaesfus@gmail.com']

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

    for i, user in enumerate(users):
        doctor = tesis_bd.Doctor(name=user, email=emails[i])
        doctor.put()

        # The record
        record = tesis_bd.Record(doctor=doctor.key, words=0, figures=0,
                                 equations=0, equations_inline=0)
        record.put()
        max_words = 30000

        for record in range(10):
            words = random.randint(1, max_words)
            figures = words/100
            equations = words/1000
            equations_inline = words/50
            date = datetime.datetime(2015, 12, record+1)
            record = tesis_bd.Record(doctor=doctor.key, words=words,
                                     figures=figures, equations=equations,
                                     equations_inline=equations_inline, date=date)
            record.put()

        # The last record
        last_record = tesis_bd.LastRecord(doctor=doctor.key, record=record.key)
        last_record.put()


# def hotfix():
#     name = "Escamilla"
#     words = 26074
#     figures = 54
#     equations = 20
#     equations_inline = 697
#     date = datetime.datetime(2015,10,28)
#
#
#     doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name==name).fetch()[0]
#     record = tesis_bd.Record(doctor=doctor.key, words=words,
#                              figures=figures, equations=equations,
#                              equations_inline=equations_inline, date=date)
#
#     record.put()

