# -*- coding: cp1252 -*-
"""
PAGINA DE HOME
"""

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
                """ Retorna la hora de la carrera (hora de Ecuador). """
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		return resultado.fechagp - datetime.timedelta(hours = 5)

	def horarioclasificacion (self):
                """ Retorna la hora en la qualy. """
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		return resultado.fechaqualy - datetime.timedelta(hours = 5)
								
	def procesar_puntos (self, resultado, predicciones):
                """ Asigna los puntos correspondientes segun la prediccion realizada. """
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
                """ Retorna la abreviacion del piloto acorde a su numero. """
		pilotos = query("SELECT * FROM Pilotos WHERE numero = :1", numero)
		piloto = pilotos.get()
		if pilotos.count() > 0:
			return piloto.abreviacion
		else:
			return ""
			
	def timemanage(self, horario_carrera, horario_clasificacion):
                """ Funcion que ayuda a determianr si aun se pueden ingresar predicciones. """
		deltalimitetiempo = datetime.timedelta(minutes = config.limitetiempo)
		limiteclasificacion = horario_clasificacion - deltalimitetiempo
		limitecarrera = horario_carrera - deltalimitetiempo
		now = datetime.datetime.now() - datetime.timedelta(hours = 5)
		return limiteclasificacion, limitecarrera, now

			
	def getuserpoints(self, username, activeusername, horario_carrera, horario_clasificacion):
                """Obtiene los puntos de cada usuario y los pone en una lista"""
                
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
                        #Obtener del la BD las predicciones para el usuario correspondiente
			predicciones = query("SELECT * FROM Predicciones WHERE usuario = :1 AND granpremio = :2", username, resultado.granpremio)

			#Calular los puntos segun las predicciones obtenidas
			ptospoleman, ptosprimero, ptossegundo, ptostercero = self.procesar_puntos(resultado, predicciones)

			#Crear listas para luego presentar los resultados en una tabla
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
					"""El usuario acutal no es el que hizo esta prediccion, pero la hora de ingreso ya ha pasado,
                                        por tanto se muestra la prediccion """
					if limiteclasificacion < now:
						prepolemans.append(self.getabr(prediccion.poleman))
					"""El usuario acutal no es el que hizo esta prediccion y la hora de ingreso no ha pasado,
                                        por tanto NO se muestra la prediccion """
					else:
						prepolemans.append("")


					"""El usuario acutal no es el que hizo esta prediccion, pero la hora de ingreso ya ha pasado,
                                        por tanto se muestra la prediccion """
					if limitecarrera < now:
						preprimeros.append(self.getabr(prediccion.primero))
						presegundos.append(self.getabr(prediccion.segundo))
						preterceros.append(self.getabr(prediccion.tercero))
					"""El usuario acutal no es el que hizo esta prediccion y la hora de ingreso no ha pasado,
                                        por tanto NO se muestra la prediccion """
					else:
						preprimeros.append("")
						presegundos.append("")
						preterceros.append("")
				else:
					prepolemans.append("")
					preprimeros.append("")
					presegundos.append("")
					preterceros.append("")

                        #El usuario actual es el que hizo la prediccion, por lo tanto siempre se muestra
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
		""" Renderizado de la pagina principal. """

		#Obtener la lista de pilotos de la BD
		pilotos = query("SELECT * FROM Pilotos ORDER BY orden ASC")
		#Convertir las horas a strings
		horacarrera = horario_carrera.strftime("%A, %d %B %Y; %I:%M %p")
		horaclasificacion = horario_clasificacion.strftime("%A, %d %B %Y; %I:%M %p")
		
                #Obtener los puntos del usuario actual
		allusers = [self.getuserpoints(user.username, user.username, horario_carrera, horario_clasificacion)]
				
                #Obtener la lista de todos los usuarios de la BD
		usuarios = query("SELECT * FROM UserInfo WHERE username != :1", user.username)
		for usuario in usuarios:
                        #Obtener los puntos de cada usuario
			allusers.append(self.getuserpoints(usuario.username, user.username, horario_carrera, horario_clasificacion))

                #Obtener los resultados (reales) del la BD
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()

		#Renderizar la pagina
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
                #Este codigo solo se ejecuto una vez para crear la tabla de pilotos
		# for piloto in config.pilotos:
			# a = Pilotos(orden = piloto.orden, numero = piloto.numero, nombre = piloto.nombre, apellido = piloto.apellido, escuderia = piloto.escuderia, abreviacion = piloto.abreviacion)
			# a.put()

		#Este codigo solo se ejecuto una vez para crear la tabla de resultados
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
                #Obtener usuario usando cookies
		user_id_cookie = self.request.cookies.get('userId')
		user_id_val = check_secure_val(user_id_cookie)
		user = UserInfo.get_by_id(int(user_id_val))

                #Obtner horario de la carrera y de la qualy
		horario_carrera = self.horariocarrera()
		horario_clasificacion = self.horarioclasificacion()

                #Obtener tiempos para determinar si se pueden ingresar predicciones
		limiteclasificacion, limitecarrera, now = self.timemanage(horario_carrera, horario_clasificacion)

                #Obtener info ingresada por el usuario en el formulario
		poleman = self.request.get("poleman")
		primero = self.request.get("primero")
		segundo = self.request.get("segundo")
		tercero = self.request.get("tercero")

                #Obtener el nombre del GP acutal
		resultados = query("SELECT * FROM Resultados WHERE actual = True")
		resultado = resultados.get()
		carrera = resultado.granpremio
		
		trampa = ""
                #Obtener la prediccion actual hecha por el usuario (si es que ya la hizo)
		predicciones = query("SELECT * FROM Predicciones WHERE usuario = :1 AND granpremio = :2", user.username, carrera)
		numpredicciones = predicciones.count()
		
                #El usuario ingreso el poleman
		if poleman != "":
			if now < limiteclasificacion:
                                #El usuario ya hizo una prediccion, por tanto se la reemplaza
				if numpredicciones > 0:
					a = predicciones.get()
					a.poleman = int(poleman)
					a.put()
				#El usuario no ha hecho una prediccion, por tanto se crea una nueva
				else:
					a = Predicciones(usuario = user.username,
						granpremio = carrera,
						fechagp = horario_carrera,
						poleman = int(poleman))
					a.put()
                        #Ya no se pueden ingresar predicciones
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar el poleman!"
				
                #El usuario ingreso el primero
		if primero != "":
			if now < limitecarrera:
                                #El usuario ya hizo una prediccion, por tanto se la reemplaza
				if numpredicciones > 0:
					a = predicciones.get()
					a.primero = int(primero)
					a.put()
				#El usuario no ha hecho una prediccion, por tanto se crea una nueva
				else:
					a = Predicciones(usuario = user.username,
								 granpremio = carrera,
								 fechagp = horario_carrera,
								 primero = int(primero))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar predicciones!"

                #El usuario ingreso el segundo
		if segundo != "":
			if now < limitecarrera:
                                #El usuario ya hizo una prediccion, por tanto se la reemplaza
				if numpredicciones > 0:
					a = predicciones.get()
					a.segundo = int(segundo)
					a.put()
				#El usuario no ha hecho una prediccion, por tanto se crea una nueva
				else:
					a = Predicciones(usuario = user.username,
								 granpremio = carrera,
								 fechagp = horario_carrera,
								 segundo = int(segundo))
					a.put()
			else:
				trampa = "No sea tramposo! Ya no se puede ingresar predicciones!"

                #El usuario ingreso el tercero
		if tercero != "":
			if now < limitecarrera:
                                #El usuario ya hizo una prediccion, por tanto se la reemplaza
				if numpredicciones > 0:
					a = predicciones.get()
					a.tercero = int(tercero)
					a.put()
                                #El usuario no ha hecho una prediccion, por tanto se crea una nueva
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
