import os
from urllib.parse import quote_plus

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ngozikama@19'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'chichindundu@gmail.com')
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'coininfinix@gmail.com')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'knkvbgxpxcnpffey')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'kjtrgujsrmedvidu')
    FLASKY_MAIL_SUBJECT_PREFIX = 'CRYPTO INVEST'
    # FLASKY_MAIL_SENDER = 'Admin tokenvault.lite@gmail.com'
    FLASKY_MAIL_SENDER = 'Admin chichindundu@gmail.com'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'richiikevin007@gmail.com')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'chijay59@gmail.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "broker-db")
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "SqlBot")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "SqlBot")
    DATABASE_DRIVER = os.environ.get("DATABASE_DRIVER", "ODBC + Driver + 17 + for +SQL + Server")

    # SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{DATABASE_USERNAME}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_HOST}/{DATABASE_NAME}?{DATABASE_DRIVER}'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev-unpaid.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-unpaid.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
