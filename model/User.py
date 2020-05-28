# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from config import app_config, app_active
from model.Role import Role
from passlib.hash import pbkdf2_sha256

config = app_config[app_active]
db = SQLAlchemy(config.APP)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=False)
    recovery_code = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Boolean(), default=1, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=False)


def get_user_by_email(self):
    return ''


def get_user_by_id(self):
    return ''


def update(self, obj):
    return ''


def hash_password(self, password):
    try:
        return pbkdf2_sha256.hash(password)
    except Exception as e:
        print("Erro ao criptografar senha %s" % e)


def set_password(self, password):
    self.password = pbkdf2_sha256.hash(password)


def verify_password(self, password_no_hash, password_database):
    try:
        return pbkdf2_sha256.verify(password_no_hash, password_database)
    except ValueError:
        return False
