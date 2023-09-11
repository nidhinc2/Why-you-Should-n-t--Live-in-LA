import os
from yaml import load, Loader
from flask import Flask
from mysql.connector.constants import ClientFlag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6d729701ba9d66cd00869242e6aff5cf9f9fcf3c53f0fa1'


def get_db_config():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open('app.yaml'), Loader=Loader)
        env_vars = variables['env_vars']
        for var in env_vars:
            os.environ[var] = env_vars[var]

    config = {
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'host': os.environ.get('MYSQL_HOST'),
        'database': os.environ.get('MYSQL_DATABASE'),
        'client_flags': [ClientFlag.SSL],
        'ssl_ca': os.environ.get('MYSQL_SSL_CA'),
        'ssl_cert': os.environ.get('MYSQL_SSL_CERT'),
        'ssl_key': os.environ.get('MYSQL_SSL_KEY')
    }

    return config


# TODO: Debug if database is connected
mysql_config = get_db_config()

from app import routes
