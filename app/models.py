from flask import current_app
from flask_login import UserMixin, current_user
from itsdangerous import URLSafeSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.BigInteger)
    country = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    btc_balance = db.Column(db.Float, default=None)
    cash_balance = db.Column(db.Float, default=None)
    level = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.btc_balance is None:
            self.btc_balance = 0.0
        if self.cash_balance is None:
            self.cash_balance = 0.0
        if self.level is None:
            self.level = 0.0

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': self.id})
    def generate_confirmation_token(self, expiration=3600):
        auth_s = Serializer(current_app.config['SECRET_KEY'])
        return auth_s.dumps({'confirm': self.id})

    # @staticmethod
    # def confirm(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.decode("utf-8"))
    #     except BadSignature:
    #         return False
    #     user = User.query.get(data.get('confirm'))
    #     if user:
    #         user.confirmed = True
    #         db.session.commit()
    #         return True
    #     return False
    @staticmethod
    def confirm(token):
        auth_s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = auth_s.loads(token)
        except BadSignature:
            return False
        user_id = data['confirm']
        user = load_user(user_id)
        # user = User.query.get(user_id)
        if user:
            user.confirmed = True
            db.session.commit()
            return True
        return False

    @property
    def is_administrator(self):
        return current_user.email == 'chijay59@gmail.com'

    def __repr__(self):
        return '<User %r>' % self.first_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
