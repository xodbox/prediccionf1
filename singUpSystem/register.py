""" Sistema de registro de usuarios. """

import webapp2
import cgi
import re
from template_handler import Handler
from cookies_manager import make_secure_val, check_secure_val
from scheme import UserInfo, query
import utilidades.bcrypt.bcrypt as bcrypt

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

#Validar valores usuario, password, pass verification e e-mail
def valid_user(user):
        """ Validar valores ingresados de usuario. """
	return USER_RE.match(user)

def valid_pass(password):
        """ Validar valores ingresados de password. """
	return PASS_RE.match(password)

def valid_verify(password, verify):
        """ Verificar que passwords sean iguales. """
	return password == verify

def valid_email(email):
        """ Verificar valores ingresados de email. """
	if not email:
		return True
	else:
		return EMAIL_RE.match(email)


class MainPage(Handler):

	def write_form(self, userError="", passError="", verifyError="", mailError="", username ="", mail = ""):
                """ Render pagina de singup. """
                
		self.render("singup.html",
								userError = userError,

								passError = passError,
								verifyError = verifyError,
								mailError = mailError,
								username = username,
								mail = mail)

	def get(self):
		self.write_form()

	def post(self):
                
		#Obtener valores ingresados por elusuario	
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

                #Validar valores ingresados por el usuario
		vuser = valid_user(username)
		vpass = valid_pass(password)
		vverify = valid_verify(password, verify)
		vemail = valid_email(email)

		userError=""
		passError=""
		verifyError=""
		emailError=""

		#hacer query en la db para ver si el ususrio existe
		vexiste = False
		user = query("SELECT * FROM UserInfo WHERE username = :1", username)
		if user.count(1) > 0:
			vuser = False
			vexiste = True

		if vuser and vpass and vverify and vemail:

			#hashear el password
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())

			#Poner info en la db y obtener la key (user id)
			a = UserInfo(username=username, password=hashed, email=email)
			a.put()
			user_id = str(a.key().id())

			#setear la cookie usando el user_id
			new_cookie_val = make_secure_val(str(user_id))
			self.response.headers.add_header('Set-Cookie', 'userId=%s, Path=/' % new_cookie_val)

			redirectTo = '/home'
			self.redirect(redirectTo)

		else:
			if not vuser:
				if vexiste:
					userError = "Ya existe ese usuario"
				else:
					userError = "Nombre de usuario invalido"
			if not vpass:
				passError = "Password invalido"
			if not vverify:
				verifyError = "Password no coincide"
			if not vemail:
				emailError = "Email incorrecto"

			self.write_form(userError, passError, verifyError, emailError, username, email)

app = webapp2.WSGIApplication([('/singup', MainPage)],
										debug=True)
