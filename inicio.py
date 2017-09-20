# -*- coding: cp1252 -*-
import webapp2
from singUpSystem.cookies_manager import check_secure_val
from singUpSystem.scheme import UserInfo

#Verifica si el usiario ha ingresado anteriormente y redirecciona a la pagina adecuada
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):

		#recuperar la cookie y el userId, chequear si es valida
		user_id_cookie = self.request.cookies.get('userId')
		if user_id_cookie:
			#chequer si es valida, si no es valida la func check_secure_val retorna None
			#si la cookie es valida, se retonrna la id del usuario
			user_id_val = check_secure_val(user_id_cookie)
			if user_id_val:
				#Acceder a la db por medio del user id
				#user = UserInfo.get_by_id(int(user_id_val))
				#self.response.out.write("<h2>Welcome %s!</h2>" % user.username)
				redirectTo = '/home'
				self.redirect(redirectTo)
			else:
				#Cookie forging?
				self.response.out.write("No sea tramposo!")
		else:
			redirectTo = '/login'
			self.redirect(redirectTo)
			
app = webapp2.WSGIApplication([ ('/', WelcomeHandler)],
										debug=True)
