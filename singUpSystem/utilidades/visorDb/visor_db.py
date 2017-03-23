#import os
#import sys

#path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
#sys.path.insert(1, path)

import webapp2
from google.appengine.ext import db
from scheme import UserInfo, query

class VisorDb(webapp2.RequestHandler):

	def get(self):
		users = query("SELECT * FROM UserInfo")
		self.response.headers['Content-Type'] = 'text/plain'
		for user in users:
			if (type(user.email) == str):
				self.response.out.write(user.username + "\t" + user.password + "\t" + user.email + "\n")
			else:
				self.response.out.write(user.username + "\t" + user.password + "\n")


app = webapp2.WSGIApplication([ ('/visordb', VisorDb)],
										debug=True)
