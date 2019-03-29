from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import jsonify
from flask import abort
import extra.auth as auth
from models import Matches


class MatchesListApi(Resource):
    def __init__(self, auth):
        super(MatchesListApi, self).__init__()
        self._auth = auth

    def get(self):
        matches = Matches.query.all()
        return jsonify(matches=[i.serialize for i in matches])

