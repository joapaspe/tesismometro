__author__ = 'jpastor'

from flask import Flask
import jinja2
import webapp2
import os
import tesis_bd
from google.appengine.ext import ndb
from google.appengine.ext import db

def initialize_bd():
    users = ["Pastor", "Flores", "Escamilla"]

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


    for user in users:
        dr = tesis_bd.Doctor(name=user)
        dr.put()

        # The record
        record = tesis_bd.Record(doctor=dr.key, words = 0, figures = 0, equations = 0, equations_inline = 0)
        record.put()

        # The last record
        last_record = tesis_bd.LastRecord(doctor=dr.key, record=record.key)
        last_record.put()
