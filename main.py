
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Adviser(ndb.Model):
    title=ndb.StringProperty(indexed=False)
    first_name=ndb.StringProperty(indexed=False)
    last_name=ndb.StringProperty(indexed=False)
    email=ndb.StringProperty(indexed=False)
    phone_number=ndb.StringProperty(indexed=False)
    department=ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('successAd.html')
        self.response.write(template.render())

class AdviserNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('adviserNew.html')
        self.response.write(template.render())

    def post(self):
        adviser = Adviser() 
        adviser.title = self.request.get('title')
        adviser.first_name= self.request.get('first_name')
        adviser.last_name = self.request.get('last_name')
        adviser.email = self.request.get('email')
        adviser.phone_number = self.request.get('phone_number')
        adviser.department = self.request.get('department')
        adviser.put()
        self.redirect('/successAd')

class AdviserDescriptionHandler(webapp2.RequestHandler):
        def get(self, adviser_id):
                adviser_all=Adviser.query().fetch()
                adviser_id = int(adviser_id)
                template_values={
                        'id': adviser_id,
                        'adviser_all': adviser_all
                }
                template = JINJA_ENVIRONMENT.get_template('adviserView.html')
                self.response.write(template.render(template_values))
 
class AdviserListHandler(webapp2.RequestHandler):
        def get(self):
                adviser_all=Adviser.query().fetch()
                template_values={
                        'adviser_all': adviser_all
                }
 
                template = JINJA_ENVIRONMENT.get_template('adviserList.html')
                self.response.write(template.render(template_values))
        

app = webapp2.WSGIApplication([
    ('/adviser/new', AdviserNewHandler),
    ('/successAd', SuccessPageHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserDescriptionHandler)
], debug=True)
