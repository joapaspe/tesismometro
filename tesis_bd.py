"""
AppEngine Database Schema
"""
__author__ = 'jpastor'
from google.appengine.ext import ndb


RECORD_FIELDS = ["words", "figures",
                 "equations", "equations_inline",
                 "cites", "pages", "date"]
RECORD_NAMES = ["Words", "Figures",
                "Equations", "Equations inline",
                "Cites", "Pages", "Date"]

record_field_to_name = {}

for i, _ in enumerate(RECORD_FIELDS):
    record_field_to_name[RECORD_FIELDS[i]] = RECORD_NAMES[i]


class Doctor(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty(default="")
    token = ndb.StringProperty(default="")


class Record(ndb.Model):
    doctor = ndb.KeyProperty(kind=Doctor)
    words = ndb.IntegerProperty(indexed=False, default=0)
    figures = ndb.IntegerProperty(default=0)
    equations = ndb.IntegerProperty(indexed=False, default=0)
    equations_inline = ndb.IntegerProperty(indexed=False, default=0)
    cites = ndb.IntegerProperty(default=0)
    pages = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty(auto_now_add=True)


class LastRecord(ndb.Model):
    doctor = ndb.KeyProperty(kind=Doctor)
    record = ndb.KeyProperty(kind=Record)




