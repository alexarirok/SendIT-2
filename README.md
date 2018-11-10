[![Build Status](https://travis-ci.org/Harrison-Gitau/SendIT-2.svg?branch=Ft-User-Fetch-All-%23161836320)](https://travis-ci.org/Harrison-Gitau/SendIT-2)
[![Coverage Status](https://coveralls.io/repos/github/Harrison-Gitau/SendIT-2/badge.svg?branch=Ft-User-Fetch-All-%23161836320)](https://coveralls.io/github/Harrison-Gitau/SendIT-2?branch=Ft-User-Fetch-All-%23161836320)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# SendIT Parcels
Gitau Parcels is a carpooling application that provides admins with the ability to create parcel oﬀers  and parcels to join available parcel oﬀers. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
$ cd into the created folder
```
  
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Initialize environment variables

```
$ export SECRET_KEY=<SECRET KEY>
```

5. Run the development server

```
$ python app.py
```

6. Navigate to [http://localhost:5000](http://localhost:5000)

At the / endpoint you should see Welcome to library books API displayed in your browser.

## Endpoints

Here is a list of all endpoints in the Gitau Parcels API

Endpoint | Functionality 
------------ | -------------
POST   /api/v1/auth/userregister | Register a user
POST   /api/v1/auth/adminregister | Register a admin
POST   /api/v1/auth/login | Log in user
POST   /api/v1/users | Create a user
GET    /api/v1/users | Get all users
GET   /api/v1/users/id/parcels | Get a single user
PUT  /api/v1/users/id/parcels | Update a single user
DELETE   /api/v1/users/id/parcels | Delete a single user
POST   /api/v1/parcels | Create new parcel
GET   /api/v1/parcels | Get all parcels
GET   /api/v1/parcels/id | Get a single parcel
PUT   /api/v1/parcels/id | Update a single parcel
POST   /api/v1/parcels/id/ | Start a parcel
DELETE   /api/v1/parcels/id | Delete a single parcel
POST   /api/v1/parcels/id/cancels | Request a parcel
GET   /api/v1/cancels | Get all cancels
DELETE   /api/v1/cancels/id | Delete a single request
GET   /api/v1/cancels/id | Get a single request
PUT  /api/v1/cancels/id | Accept/Reject a request

## Running the tests

To run the automated tests simply run

```
nosetests tests
```

### And coding style tests

Coding styles tests are tests that ensure conformity to coding style guides. In our case, they test conformity to
PEP 8 style guides

```
pylint app.py
```

## Deployment

Ensure you use Productionconfig settings which have DEBUG set to False

## Built With

* HTML5
* CSS3
* Python 3.6.4
* Flask - The web framework used

## GitHub pages

https://Gitau.github.io/

## Heroku


## Versioning

Most recent version is version 1

## Authors

Gitau Harrison.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration and encouragement
* etc
