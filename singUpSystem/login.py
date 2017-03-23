import webapp2
import cgi
import re
from template_handler import Handler
from cookies_manager import make_secure_val, check_secure_val
from scheme import UserInfo, query
import utilidades.bcrypt.bcrypt as bcrypt

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")

#Validar valores usuario, password, pass verification e e-mail
def valid_user(user):
	return USER_RE.match(user)

def valid_pass(password):
	return PASS_RE.match(password)

class MainPage(Handler):

	def write_form(self, userError="", passError="", loginError =""):
		self.render(	"login.html",
						userError = userError,
						passError = passError,
						loginError = loginError)

	def validate(self, username, password):
		#hacer query en la db para ver si el ususrio existe
		users = query("SELECT * FROM UserInfo WHERE username = :1", username)
		for user in users:
			#Verificar el password
			if bcrypt.hashpw(password, user.password) == user.password:
				return str(user.key().id())
		return None

	def get(self):
		self.write_form()

	def post(self):
			
		username = self.request.get("username")
		password = self.request.get("password")

		vuser = valid_user(username)
		vpass = valid_pass(password)
		
		if vuser and vpass:
			user_id = self.validate(username, password)
		else:
			user_id = None

		userError=""
		passError=""
		loginError = ""

		if vuser and vpass and user_id:

			new_cookie_val = make_secure_val(str(user_id))
			self.response.headers.add_header('Set-Cookie', 'userId=%s, Path=/' % new_cookie_val)

			redirectTo = '/home'
			self.redirect(redirectTo)

		else:
			if not vuser:
				userError = "Nombre de usuario invalido"
			if not vpass:
				passError = "Password invalido"
			if not user_id:
				loginError = "Usuario/Password incorrecto"

			self.write_form(userError, passError, loginError)

app = webapp2.WSGIApplication([('/login', MainPage)],
										debug=True)
