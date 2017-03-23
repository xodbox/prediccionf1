from google.appengine.ext import db

class Predicciones(db.Model):
	usuario = db.StringProperty(required = True)
	granpremio = db.StringProperty(required = True)
	creado = db.DateTimeProperty(auto_now = True)
	poleman = db.IntegerProperty()
	primero = db.IntegerProperty()
	segundo = db.IntegerProperty()
	tercero = db.IntegerProperty()
	
class Resultados(db.Model):
	granpremio = db.StringProperty(required = True)
	fechagp = db.DateTimeProperty(required = True)
	fechaqualy = db.DateTimeProperty(required = True)
	poleman = db.IntegerProperty(required = True)
	primero = db.IntegerProperty(required = True)
	segundo = db.IntegerProperty(required = True)
	tercero = db.IntegerProperty(required = True)
	actual = db.BooleanProperty(required = True)
	
class Pilotos(db.Model):
	orden = db.IntegerProperty(required = True)
	numero = db.IntegerProperty(required = True)
	nombre = db.StringProperty(required = True)
	apellido = db.StringProperty(required = True)
	escuderia = db.StringProperty(required = True)
	abreviacion = db.StringProperty(required = True)

def query(q, *a, **kw):
	return db.GqlQuery(q, *a, **kw)
