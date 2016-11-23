# @@@ separate wsgi middlewares from django middlewares
# to avoid app loading errors
import re


class WSGITeamMiddleware(object):

    def __init__(self, application):
        self.app = application

    def __call__(self, environ, start_repsonse):
        m = re.match(r"(/teams/([\w-]+))(.*)", environ["PATH_INFO"])
        if m:
            environ["SCRIPT_NAME"] = m.group(1)
            environ["PATH_INFO"] = m.group(3)
            environ["pinax.team"] = m.group(2)
        return self.app(environ, start_repsonse)
