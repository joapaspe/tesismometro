__author__ = 'jpastor'
import cgi, urllib

from google.appengine.ext import ndb


record_fields = ["words", "figures", "equations", "equations_inline","cites","pages","date"]
record_names = ["Words", "Figures", "Equations", "Equations inline","Cites","Pages", "Date"]
class Doctor(ndb.Model):
    name = ndb.StringProperty()


class Record(ndb.Model):

    doctor = ndb.KeyProperty(kind=Doctor)
    words = ndb.IntegerProperty(indexed=False)
    figures = ndb.IntegerProperty()
    equations = ndb.IntegerProperty(indexed=False)
    equations_inline = ndb.IntegerProperty(indexed=False)
    cites = ndb.IntegerProperty(default=0)
    pages = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty(auto_now_add=True)



class LastRecord(ndb.Model):

    doctor = ndb.KeyProperty(kind=Doctor)
    record = ndb.KeyProperty(kind=Record)




