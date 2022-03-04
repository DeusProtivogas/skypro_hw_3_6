from flask import request, abort
from flask_restx import Namespace, Resource

from service.auth import get_tokens, get_refresh_tokens

auth_ns = Namespace("auth")

@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        if not request.json:
            abort(400, "Bad request")
        tokens = get_tokens(request.json)
        if tokens:
            return tokens, 200
        abort(401, "Authorizations error")

    def put(self):
        if not request.json:
            abort(400, "Bad request")
        tokens = get_refresh_tokens(request.json)
        if tokens:
            return tokens, 200
        abort(401, "Authorizations error")