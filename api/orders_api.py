from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import jsonify
from flask import abort
import extra.auth as auth
from models import Orders


class OrdersApi(Resource):
    def __init__(self, auth):
        super(OrdersApi, self).__init__()
        self._auth = auth

    def get(self, id):
        orders = Orders.query.filter_by(id=id).first()
        if not orders:
            abort(404)
        return jsonify(orders.serialize)

