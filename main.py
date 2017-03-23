import os
import webapp2
import datetime
from collections import namedtuple

import handler
import config
from singUpSystem.cookies_manager import check_secure_val
from singUpSystem.scheme import UserInfo
from scheme import Predicciones, Resultados, Pilotos, query

UserPoints = namedtuple('UserPoints', [  'ptostotales', 'grandespremios', 'ptospolemans', 'ptosprimeros', 'ptossegundos', 'ptosterceros', 'ptosdelosgps',
										'realpolemans', 'realprimeros', 'realsegundos', 'realterceros',
										'prepolemans', 'preprimeros', 'presegundos', 'preterceros', 'size', 'usuario'])

			   							   
class MainPage(handler.Handler):

	def horariocarrera (self):
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		return resultado.fechagp - datetime.timedelta(hours = 5)

	def horarioclasificacion (self):
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		return resultado.fechaqualy - datetime.timedelta(hours = 5)
								
	def procesar_puntos (self, resultado, predicciones):		
		if predicciones.count() > 0:
			prediccion = predicciones.get()

			if(resultado.poleman == prediccion.poleman):
				ptospoleman = 5
			else:
				ptospoleman = 0

			if(resultado.primero == prediccion.primero):
				ptosprimero = 25
			else:
				ptosprimero = 0

			if(resultado.segundo == prediccion.segundo):
				ptossegundo = 18
			else:
				ptossegundo = 0

			if(resultado.tercero == prediccion.tercero):
				ptostercereo = 15
			else:
				ptostercereo= 0

		else:
			ptospoleman = 0
			ptosprimero = 0
			ptossegundo = 0
			ptostercereo = 0
			
		return ptospoleman, ptosprimero, ptossegundo, ptostercereo
	
	def getabr(self, numero):
		pilotos = query("SELECT * FROM Pilotos WHERE numero = :1", numero)
		piloto = pilotos.get()
		if pilotos.count() > 0:
			return piloto.abreviacion
		else:
			return ""
			
	def timemanage(self, horario_carrera, horario_clasificacion):
		deltalimitetiempo = datetime.timedelta(minutes = config.limitetiempo)
		limiteclasificacion = horario_clasificacion - deltalimitetiempo
		limitecarrera = horario_carrera - deltalimitetiempo
		now = datetime.datetime.now() - datetime.timedelta(hours = 5)
		return limiteclasificacion, limitecarrera, now

			
	def getuserpoints(self, username, activeusername, horario_carrera, horario_clasificacion):
		limiteclasificacion, limitecarrera, now = self.timemanage(horario_carrera, horario_clasificacion)

		resultados = query("SELECT * FROM Resultados ORDER BY fechagp DESC")
		ptostotales = 0
		grandespremios = []
		ptospolemans = []
		ptosprimeros = []
		ptossegundos = []
		ptosterceros = []
		ptosdelosgps = []
		realpolemans = []
		realprimeros = []
		realsegundos = []
		realterceros = []
		prepolemans = []
		preprimeros = []
		presegundos = []
		preterceros = []

		for resultado in resultados:
			predicciones = query("SELECT * FROM Predicciones WHERE usuario = :1 AND granpremio = :2", username, resultado.granpremio)
			ptospoleman, ptosprimero, ptossegundo, ptostercero = self.procesar_puntos(resultado, predicciones)
			grandespremios.append(resultado.granpremio)
			ptospolemans.append(ptospoleman)
			ptosprimeros.append(ptosprimero)
			ptossegundos.append(ptossegundo)
			ptosterceros.append(ptostercero)
			ptosdelosgps.append(ptospoleman + ptosprimero + ptossegundo + ptostercero)
			ptostotales += ptospoleman + ptosprimero + ptossegundo + ptostercero
			realpolemans.append(self.getabr(resultado.poleman))
			realprimeros.append(self.getabr(resultado.primero))
			realsegundos.append(self.getabr(resultado.segundo))
			realterceros.append(self.getabr(resultado.tercero))
			
			if username != activeusername and resultado.actual == True:
				if predicciones.count() > 0:
					prediccion = predicciones.get()
					if limiteclasificacion < now:
						prepolemans.append(self.getabr(prediccion.poleman))
					else:
						prepolemans.append("")
					if limitecarrera < now:
						preprimeros.append(self.getabr(prediccion.primero))
						presegundos.append(self.getabr(prediccion.segundo))
						preterceros.append(self.getabr(prediccion.tercero))
					else:
						preprimeros.append("")
						presegundos.append("")
						preterceros.append("")
				else:
					prepolemans.append("")
					preprimeros.append("")
					presegundos.append("")
					preterceros.append("")
			else:
				if predicciones.count() > 0:
					prediccion = predicciones.get()
					prepolemans.append(self.getabr(prediccion.poleman))
					preprimeros.append(self.getabr(prediccion.primero))
					presegundos.append(self.getabr(prediccion.segundo))
					preterceros.append(self.getabr(prediccion.tercero))
				else:
					prepolemans.append("")
					preprimeros.append("")
					presegundos.append("")
					preterceros.append("")
				
		
		return UserPoints (ptostotales, grandespremios, ptospolemans, ptosprimeros, ptossegundos, ptosterceros, ptosdelosgps,
							realpolemans, realprimeros, realsegundos, realterceros,
							prepolemans, preprimeros, presegundos, preterceros, len(grandespremios), username)

	def pagina(self, horario_carrera, horario_clasificacion, user, trampa):
		limiteclasificacion, limitecarrera, now = self.timemanage(horario_carrera, horario_clasificacion)
		
		pilotos = query("SELECT * FROM Pilotos ORDER BY orden ASC")
		horacarrera = horario_carrera.strftime("%A, %d %B %Y; %I:%M %p")
		horaclasificacion = horario_clasificacion.strftime("%A, %d %B %Y; %I:%M %p")
		
		allusers = [self.getuserpoints(user.username, user.username, horario_carrera, horario_clasificacion)]
				
		usuarios = query("SELECT * FROM UserInfo WHERE username != :1", user.username)
		for usuario in usuarios:
			allusers.append(self.getuserpoints(usuario.username, user.username, horario_carrera, horario_clasificacion))

		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
			
		self.render('main.html', usuario = user.username,
						horario_carrera=horacarrera,
						horario_clasificacion=horaclasificacion,
						pilotos = pilotos,
						carrera = resultado.granpremio,
						limitetiempo = config.limitetiempo + 1,
						limiteclasificacion = limiteclasificacion,
						limitecarrera = limitecarrera,
						now = now,
						trampa = trampa,
						allusers = allusers)

	def get(self):
		# for piloto in config.pilotos:
			# a = Pilotos(orden = piloto.orden, numero = piloto.numero, nombre = piloto.nombre, apellido = piloto.apellido, escuderia = piloto.escuderia, abreviacion = piloto.abreviacion)
			# a.put()
		
		# a = Resultados(granpremio = config.carrera, fechagp = datetime.datetime(year=2016, month = 7, day = 10), fechaqualy = datetime.datetime(year=2016, month = 7, day = 15), poleman = 0, primero = 0, segundo = 0, tercero = 0, actual = True)
		# a.put()
			
		#recuperar la cookie y el userId, chequear si es valida
		user_id_cookie = self.request.cookies.get('userId')
		if user_id_cookie:
			#chequer si es valida, si no es valida la func check_secure_val retorna None
			#si la cookie es valida, se retonrna la id del usuario
			user_id_val = check_secure_val(user_id_cookie)
			if user_id_val:
				#Acceder a la db por medio del user id
				user = UserInfo.get_by_id(int(user_id_val))
				horario_carrera = self.horariocarrera()
				horario_clasificacion = self.horarioclasificacion()
				
				self.pagina(horario_carrera = horario_carrera, 
							horario_clasificacion = horario_clasificacion,
							user = user,
							trampa = "")

			else:
				#Cookie forging?
				self.response.out.write("No sea tramposo!")
		else:
			redirectTo = '/login'
			self.redirect(redirectTo)

	def post (self):
		user_id_cookie = self.request.cookies.get('userId')
		user_id_val = check_secure_val(user_id_cookie)
		user = UserInfo.get_by_id(int(user_id_val))

		horario_carrera = self.horariocarrera()
		horario_clasificacion = self.horarioclasificacion()

		limiteclasificacion, limitecarrera, now = self.timemanage(horario_carrera, horario_clasificacion)

		poleman = self.request.get("poleman")
		primero = self.request.get("primero")
		segundo = self.request.get("segundo")
		tercero = self.request.get("tercero")

		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		carrera = resultado.granpremio
		
		trampa = ""
		predicciones = query("SELECT * FROM Predicciones WHERE usuario = :1 AND granpremio = :2", user.username, carrera)
		numpredicciones = predicciones.count()
		
		if poleman != "":
			if now < limiteclasificacion:
				if numpredicciones > 0:
					a = predicciones.get()
					a.poleman = int(poleman)
					a.put()
				else:
					a = Predicciones(usuario = user.username,
						granpremio = carrera,
						fechagp = horario_carrera,
						poleman = int(poleman))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar el poleman!"
				
		if primero != "":
			if now < limitecarrera:
				if numpredicciones > 0:
					a = predicciones.get()
					a.primero = int(primero)
					a.put()
				else:
					a = Predicciones(usuario = user.username,
								 granpremio = carrera,
								 fechagp = horario_carrera,
								 primero = int(primero))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar predicciones!"

		if segundo != "":
			if now < limitecarrera:
				if numpredicciones > 0:
					a = predicciones.get()
					a.segundo = int(segundo)
					a.put()
				else:
					a = Predicciones(usuario = user.username,
								 granpremio = carrera,
								 fechagp = horario_carrera,
								 segundo = int(segundo))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar predicciones!"

		if tercero != "":
			if now < limitecarrera:
				if numpredicciones > 0:
					a = predicciones.get()
					a.tercero = int(tercero)
					a.put()
				else:
					a = Predicciones(usuario = user.username,
								 granpremio = carrera,
								 fechagp = horario_carrera,
								 tercero = int(tercero))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar predicciones!"

		redirectTo = '/home'
		self.redirect(redirectTo)

app = webapp2.WSGIApplication([
    ('/home', MainPage),
], debug=True)
