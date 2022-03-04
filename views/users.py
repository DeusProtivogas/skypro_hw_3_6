from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from service.auth import auth_required, admin_required

user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()

        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return f"Created user {user.id}!", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        b = user_service.get_one(uid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    @auth_required
    @admin_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    @auth_required
    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
