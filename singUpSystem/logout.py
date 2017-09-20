import webapp2

class MainPage(webapp2.RequestHandler):

	def get(self):
                """ Log out de la cuenta. """
		self.response.headers.add_header('Set-Cookie', 'userId="", Path=/')
		redirectTo = '/'
		self.redirect(redirectTo)

app = webapp2.WSGIApplication([ ('/logout', MainPage)],
										debug=True)
