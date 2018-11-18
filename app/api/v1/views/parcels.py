"""Contains all endpoints to manipulate parcel information
"""
from flask import request, jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse
import jwt


from ..models import users, parcels
from instance import config
from ..utils.decorators import user_required, admin_required


class ParcelList(Resource):
    """Contains GET and POST methods"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'pickup_location',
            required=True,
            type=str,
            help='kindly provide a departure point',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'destination_location',
            required=True,
            type=str,
            help="kindly provide a valid destination_location",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'date_ordered',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'max',
            required=True,
            type=int,
            help="kindly provide a valid integer of the max number of parcels",
            location=['form', 'json'])
        super().__init__()

    @user_required
    def post(self):
        """Adds a new parcel"""
        kwargs = self.reqparse.parse_args()

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        result = parcels.Parcel.create_parcel(userid=user_id, **kwargs)
        return make_response(jsonify(result), 201)

    @admin_required
    def get(self):
        """Gets all parcels"""
        return make_response(jsonify(parcels.all_parcels), 200)

class Parcel(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single parcel"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'pickup_location',
            required=True,
            type=str,
            help='kindly provide a departure point',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'destination_location',
            required=True,
            type=str,
            help="kindly provide a valid destination_location",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'date_ordered',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            location=['form', 'json'])
        self.reqparse.add_argument(
            'max',
            required=True,
            location=['form', 'json'])
        super().__init__()

    def get(self, parcel_id):
        """Get a particular parcel"""
        try:
            parcel = parcels.all_parcels[parcel_id]
            return make_response(jsonify(parcel), 200)
        except KeyError:
            return make_response(jsonify({"message" : "parcel does not exist"}), 404)

    @user_required
    def post(self, parcel_id):
        """start a particular parcel"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        result = parcels.Parcel.start_parcel_delivery(parcel_id, user_id=user_id)
        if result == {"message" : "parcel delivery started"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

    @user_required
    def put(self, parcel_id):
        """Update a particular parcel"""
        kwargs = self.reqparse.parse_args()

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        result = parcels.Parcel.update_parcel(parcel_id, userid=user_id, **kwargs)
        if result != {"message" : "parcel does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

    @admin_required
    def delete(self, parcel_id):
        """Delete a particular parcel"""
        result = parcels.Parcel.delete_parcel(parcel_id)
        if result != {"message" : "the parcel does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

class RequestParcel(Resource):
    """Contains POST method for requesting a particular parcel"""


    @user_required
    def post(self, parcel_id):
        """Request a particular parcel"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        result = parcels.Requests.request_parcel(parcel_id=parcel_id, user_id=user_id)
        return make_response(jsonify(result), 201)

class RequestList(Resource):
    """Contains GET method to get all cancels"""

    @admin_required
    def get(self):
        """Gets all cancels"""
        return make_response(jsonify(parcels.all_cancels), 200)

class Request(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single request"""


    @user_required
    def get(self, request_id):
        """Get a particular request"""
        try:
            parcel = parcels.all_cancels[request_id]
            return make_response(jsonify(parcel), 200)
        except KeyError:
            return make_response(jsonify({"message" : "specified request does not exist"}), 404)

    @admin_required
    def put(self, request_id):
        """accept/reject a particular request"""

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin_id = data['id']


        result = parcels.all_cancels.get(request_id)
        if result != None:
            if parcels.all_parcels[result["parcel_id"]]["admin_id"] == admin_id:
                update = parcels.Requests.update_request(request_id)
                return make_response(jsonify(update), 200)
            return make_response(jsonify({
                "message" : "the parcel request you are updating is not of your parcel"}), 404)
        return make_response(jsonify({"message" : "the parcel request does not exist"}), 404)

    @user_required
    def delete(self, request_id):
        """Delete a particular request"""

        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        currentuser_id = data['id']

        result = parcels.all_cancels.get(request_id)
        if result != None:
            if result["user_id"] == currentuser_id:
                delete = parcels.Requests.delete_request(request_id)
                return make_response(jsonify(delete), 200)
            return make_response(jsonify({
                "message" : "the parcel request you are deleting is not your request"}), 404)
        return make_response(jsonify({"message" : "the parcel request does not exist"}), 404)

parcels_api = Blueprint('resources.parcels', __name__)
api = Api(parcels_api)
api.add_resource(ParcelList, '/parcels', endpoint='parcels')
api.add_resource(Parcel, '/parcels/<int:parcel_id>', endpoint='parcel')
api.add_resource(RequestParcel, '/parcels/<int:parcel_id>/cancels', endpoint='requestparcel')
api.add_resource(RequestList, '/cancels', endpoint='cancels')
api.add_resource(Request, '/cancels/<int:request_id>', endpoint='request')