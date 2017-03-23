from google.appengine.ext import db

class UserInfo(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty

def query(*q):
	if len(q) == 1:
		return db.GqlQuery(q[0])
	else:
		return db.GqlQuery(q[0], q[1])
