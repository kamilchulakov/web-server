from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import jsonify
from flask import abort
import extra.auth as auth
from models import Storage


class StorageApi(Resource):
    def __init__(self, auth):
        super(StorageApi, self).__init__()
        self._auth = auth

    def get(self):
        storage = Storage.query.all()
        return jsonify(storage=[i.serialize for i in storage])
