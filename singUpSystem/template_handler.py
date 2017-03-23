import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
								autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, a):
		self.response.out.write(a)

	def render(self, template, **kw):
		t = jinja_env.get_template(template)
		self.write(t.render(kw))
