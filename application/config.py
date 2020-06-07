# -*- config:utf-8 -*-

import logging
from datetime import timedelta
from os import urandom as secrete

import configparser

config = configparser.ConfigParser()

config.read('.ini')

default = config['DEFAULT']

project_name = 'download_api'


class Config(object):
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = default['port'] or '5000'

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = default['secret_key'] or secrete(16)

    # LOGGING
    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "%s/app.%s.log" % (default['log_path'], project_name)
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # DOCUMENTS PATH
    DOCUMENTS_FOLDER = default['files_folder']

    DATE_PATTERN = '%d/%m/%Y - %H:%M:%S'


class Dev(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # log all statements issued
