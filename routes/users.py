import flask
from flask import jsonify, abort, request, Blueprint

import db.couchDB_service as db

users_route = Blueprint('users-route', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_route


# Not quite done, must send to_public()
@users_route.route('/', methods=['GET'])
def get_all():
    return jsonify(db.get_users())


# Done -> check token
@users_route.route('/<string:_id>', methods=['GET'])
def get_with_id(_id):
    user = db.get_user_by_id(_id)
    return jsonify(user.to_public()) if user else flask.abort(404)


@users_route.route('/<string:_id>/ban', methods=['POST'])
def ban(_id):
    if not request.get_json():
        return jsonify(db.ban_user(None))

    data = request.get_json(force=True)

    return jsonify(db.ban_user(data))


# Done -> mais à checker
@users_route.route('/', methods=['POST'])
def create_one():
    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)
    print(data)
    return jsonify(db.create_user(data))


@users_route.route('/<string:_id>', methods=['DELETE'])
def delete_one(_id):
    return jsonify(db.delete_user(_id))


@users_route.route('/<string:_id>', methods=['PUT'])
def edit_one(_id):
    if not request.get_json():
        abort(400)

    # data = request.get_json(force=True)

    return jsonify(db.edit_user())
