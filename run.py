"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os

from flask import Flask

from app import create_app


app = create_app('instance.config.ProductionConfig')


@app.route('/')
def hello_world():
    """Tests running of the flask app"""
    
    return 'Welcome to SendIT :: v1 ! Parcel Delivery Order Service !'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
