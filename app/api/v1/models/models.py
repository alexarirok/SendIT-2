"""Handles data storage for Users, parcels and cancels
"""

from werkzeug.security import generate_password_hash


all_users = {1 : {"id": "1", 
                  "username" : "admin",
                  "email" : "admin@gmail.com",
                  "password" : generate_password_hash("adminU234", method='sha256'),
                  "usertype" : "admin",},}
user_count = 2

all_parcels = {}
parcel_count = 1

all_cancels = {}
request_count = 1

class User(object):
    """Contains methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, usertype):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_count
        password = generate_password_hash(password, method='sha256')
        all_users[user_count] = {
            "id": user_count, 
            "username" : username,
            "email" : email, 
            "password" : password, 
            "usertype" : usertype}
        new_user = all_users[user_count]
        user_count += 1
        return new_user


    @staticmethod
    def update_user(user_id, usertype, username, email, password):
        """Updates user information"""
        if user_id in all_users.keys():
            all_users[user_id] = {"id" : user_id, "username" : username,
                                  "email" : email, "password" : password,
                                  "usertype" : usertype}
            return all_users[user_id]
        return {"message" : "user does not exist"}

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            del all_users[user_id]
            return {"message" : "user successfully deleted"}
        except KeyError:
            return {"message" : "user does not exist"}

    @staticmethod
    def all_users():
        """get all users"""

        users = []
        for user in all_users:
            user = all_users[user]

            if user["usertype"] == "adminU":
                profile = {user['id'] : {
                    "Username" : user['username'], 
                    "Email" : user['email'],
                    "Usertype" : user['usertype'],
                    "Parcels already IN TRANSIT" : [], 
                    "Parcels UNDELIVERED" : []}}
                    
                for parcel in all_parcels:
                    parcel = all_parcels[parcel]
                    if parcel["adminU_id"] == user["id"]:
                        if parcel["status"] == "IN TRANSIT":
                            profile[user['id']]["Parcels already IN TRANSIT"].append(parcel["trip"])
                        profile[user['id']]["Parcels UNDELIVERED"].append(parcel["trip"])
            else:
                profile = {user['id'] : {'username' : user['username'], 'email' : user['email'],
                                         'usertype' : user['usertype'],
                                         'Parcels already DELIVERED' : [],
                                         'Parcels UNDELIVERED' : [], 'Parcels CANCELED' : []}}
                for request in all_cancels:
                    request = all_cancels[request]
                    if request["user_id"] == user["id"]:
                        triprequest = all_parcels[request["parcel_id"]]["trip"]
                        if request["status"] == "CANCELED":
                            profile[user['id']]["Parcels already CANCELED"].append(triprequest)
                        if request["status"] == "UNDELIVERED":
                            profile[user['id']]["Parcels UNDELIVERED"].append(triprequest)
                        if request["status"] == "DELIVERED":
                            profile[user['id']]["Parcels DELIVERD"].append(triprequest)

            users.append(profile)

        return {"all_users" : users}

    @staticmethod
    def get_user(user_id):
        """get a user"""

        user = all_users[user_id]

        if user["usertype"] == "adminU":
            profile = {user['id'] : {"Username" : user['username'], "Email" : user['email'],
                                     "Usertype" : user['usertype'],
                                     "Parcels already IN TRANSIT" : [], "Parcels UNDELIVERED" : []}}

            for parcel in all_parcels:
                parcel = all_parcels[parcel]
                if parcel["adminU_id"] == user_id:
                    if parcel["status"] == "IN TRANSIT":
                        profile[user['id']]["Parcels already IN TRANSIT"].append(parcel["trip"])
                    profile[user['id']]["Parcels UNDELIVERED"].append(parcel["trip"])
                return profile

        else:
            profile = {user['id'] : {"username" : user['username'], "email" : user['email'],
                                     "usertype" : user['usertype'],
                                     "Parcels already DELIVERED" : [], "Parcels UNDELIVERED" : [],
                                     "Parcels CANCELED" : []}}
            for request in all_cancels:
                request = all_cancels[request]
                if request["user_id"] == user_id:
                    triprequest = all_parcels[request["parcel_id"]]["trip"]
                    if request["status"] == "DELIVERED":
                        profile[user['id']]["Parcels already DELIVERED"].append(triprequest)
                    if request["status"] == "UNDELIVERED":
                        profile[user['id']]["Parcels UNDELIVERED"].append(triprequest)
                    if request["status"] == "CANCELED":
                        profile[user['id']]["Parcels CANCELED"].append(triprequest)
                return profile
        return profile



class Parcel(object):
    """Contains methods to add, update and delete a parcel"""


    @staticmethod
    def create_parcel(pickup_location, destination_location, adminUid, date_ordered, price,
                    max, status="UNDELIVERED"):
        """Creates a parcel and appends this information to parcels dictionary"""
        global all_parcels
        global parcel_count
        all_parcels[parcel_count] = {"id": parcel_count, "trip" : pickup_location + " to " + destination_location,
                                 "adminU_id": adminUid, "date_ordered": date_ordered,
                                 "price": price, "max": max,
                                 "parcels" : [], "status" : status}
        new_parcel = all_parcels[parcel_count]
        parcel_count += 1
        return new_parcel

    @staticmethod
    def update_parcel(parcel_id, pickup_location, destination_location, adminUid, date_ordered, price, max):
        """Updates parcel information"""

        if parcel_id in all_parcels.keys():
            parcels = all_parcels[parcel_id]["parcels"]
            status = all_parcels[parcel_id]["status"]
            all_parcels[parcel_id] = {"id": parcel_id, "trip" : pickup_location + " to " + destination_location,
                                  "adminU_id": adminUid, "date_ordered": date_ordered,
                                  "price": price, "max": max,
                                  "parcels": parcels, "status" : status}
            return all_parcels[parcel_id]
        return {"message" : "parcel does not exist"}

    @staticmethod
    def start_parcel_delivery(parcel_id, adminU_id):
        """starts a parcel delivery"""

        if parcel_id in all_parcels.keys():

            if all_parcels[parcel_id]["adminU_id"] == adminU_id:
                all_parcels[parcel_id]["status"] = "IN TRANSIT"

                for request in all_cancels:
                    request = all_cancels[request]
                    if request["parcel_id"] == parcel_id:
                        if request["cancel_order"] is True:
                            request["status"] = "CANCELED"
                        elif request["cancel_order"] is False:
                            request["status"] = "DELIVERED"

                return {"message" : "parcel delivery started"}

            return {"message" : "The parcel delivery you want to start is not your parcel."}
        return {"message" : "parcel does not exist"}

    @staticmethod
    def delete_parcel(parcel_id):
        """Deletes a parcel"""
        try:
            del all_parcels[parcel_id]
            for request in all_cancels:
                request = all_cancels[request]
                if request["parcel_id"] == parcel_id:
                    request["status"] = "parcel deleted"

            return {"message" : "the parcel successfully deleted"}
        except KeyError:
            return {"message" : "the parcel does not exist"}


class Requests(object):
    """Contains methods to add, update and delete cancels"""


    @staticmethod
    def request_parcel(parcel_id, user_id, cancel_order=False, status="UNDELIVERED"):
        """Creates a new request and appends this information to the all_cancels dictionary"""
        global all_cancels
        global request_count
        all_cancels[request_count] = {"id": request_count, "parcel_id" : parcel_id, "user_id": user_id,
                                       "cancel_order": cancel_order, "status" : status}
        request_count += 1

        return {"message" : "the request has been sent for approval"}

    @staticmethod
    def update_request(request_id):
        """Updates request information in all_cancels dictionary"""
        max = int(all_parcels[all_cancels[request_id]["parcel_id"]]["max"])
        cancel_order = all_parcels[all_cancels[request_id]["parcel_id"]]["parcels"]
        parcels = int(len(cancel_order))

        if parcels < max:
            if all_cancels[request_id]["cancel_order"] is False:
                all_cancels[request_id]["cancel_order"] = True
                cancel_order.append(all_users[all_cancels[request_id]["user_id"]]["username"])
                return {"message" : "the request has been cancel_order"}

            elif all_cancels[request_id]["cancel_order"] is True:
                all_cancels[request_id]["cancel_order"] = False
                cancel_order.remove(all_users[all_cancels[request_id]["user_id"]]["username"])
                return {"message" : "the request has been CANCELED"}
        else:
            if all_cancels[request_id]["cancel_order"] is True:
                all_cancels[request_id]["cancel_order"] = False
                cancel_order.remove(all_users[all_cancels[request_id]["user_id"]]["username"])
                return {"message" : "the request has been CANCELED"}
            return {"message" : "the parcel has reached its max number of parcels"}

    @staticmethod
    def delete_request(request_id):
        """Deletes a request from the all request dictionary"""
        try:
            del all_cancels[request_id]
            return {"message" : "request successfully deleted"}
        except KeyError:
            return {"message" : "the specified request does not exist in cancels"}