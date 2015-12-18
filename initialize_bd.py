__author__ = 'jpastor'

from flask import Flask
import jinja2
import webapp2
import os
import tesis_bd
from google.appengine.ext import ndb
from google.appengine.ext import db
import datetime


def initialize_bd():
    users = ["Pastor", "Flores", "Escamilla"]
    emails = ["joapaspe@gmail.com", "enflosae@gmail.com", "joaesfus@gmail.com"]
    rec = {
          'words': 0,
          'figures': 0,
          'equations_inline': 0,
          'equations': 0,

         }

    # Remove data
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
        dr = tesis_bd.Doctor(name=user, email=emails[i])
        dr.put()

        # The record
        record = tesis_bd.Record(doctor=dr.key, words = 0, figures = 0, equations = 0, equations_inline = 0)
        record.put()

        import random
        max_words = random.randint(1, 30000)

        for i in range(10):
            words = random.randint(1, 30000)
            figures = words/100
            equations = words/1000
            equations_inline = words/50
            date = datetime.datetime(2015,12,i+1)
            record = tesis_bd.Record(doctor=dr.key, words=words, figures=figures, equations=equations, equations_inline=equations_inline, date=date)
            record.put()

        # The last record
        last_record = tesis_bd.LastRecord(doctor=dr.key, record=record.key)
        last_record.put()


def hotfix():
    name = "Escamilla"
    words = 26074
    figures = 54
    equations = 20
    equations_inline = 697
    date = datetime.datetime(2015,10,28)


    doctor = tesis_bd.Doctor.query(tesis_bd.Doctor.name==name).fetch()[0]
    record = tesis_bd.Record(doctor=doctor.key, words=words, figures=figures, equations=equations, equations_inline=equations_inline, date=date)

    record.put()