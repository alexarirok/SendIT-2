from werkzeug.security import generate_password_hash
from .parcels import all_parcels, all_cancels

all_users = {1 : {"id": "1", 
                  "username" : "admin",
                  "email" : "admin@gmail.com",
                  "password" : generate_password_hash("admin234", method='sha256'),
                  "usertype" : "admin",},}
user_count = 2
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

            if user["usertype"] == "admin":
                profile = {user['id'] : {
                    "Username" : user['username'], 
                    "Email" : user['email'],
                    "Usertype" : user['usertype'],
                    "Parcels already IN TRANSIT" : [], 
                    "Parcels UNDELIVERED" : []}}
                    
                for parcel in all_parcels:
                    parcel = all_parcels[parcel]
                    if parcel["admin_id"] == user["id"]:
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

        if user["usertype"] == "admin":
            profile = {user['id'] : {"Username" : user['username'], "Email" : user['email'],
                                     "Usertype" : user['usertype'],
                                     "Parcels already IN TRANSIT" : [], "Parcels UNDELIVERED" : []}}

            for parcel in all_parcels:
                parcel = all_parcels[parcel]
                if parcel["admin_id"] == user_id:
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





