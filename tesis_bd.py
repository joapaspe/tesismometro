__author__ = 'jpastor'
import cgi, urllib

from google.appengine.ext import ndb


record_fields = ["name", "words", "figures", "equations", "equations_inline"]
class Doctor(ndb.Model):
    name = ndb.StringProperty()


class Record(ndb.Model):

    doctor = ndb.KeyProperty(kind=Doctor)
    words = ndb.IntegerProperty(indexed=False)
    figures = ndb.IntegerProperty()
    equations = ndb.IntegerProperty(indexed=False)
    equations_inline = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now=True)



class LastRecord(ndb.Model):

    doctor = ndb.KeyProperty(kind=Doctor)
    record = ndb.KeyProperty(kind=Record)




