import hashlib
import re
from contextlib import suppress
from datetime import datetime
from loguru import logger

from peewee import DoesNotExist, CharField, DateTimeField, BooleanField

from utils import not_empty, not_none
from models import DBModel, insure_connect

# user role
Admin = "Admin"
Operator = "Operator"
Guest = "Guest"

GuestEmail = "guest@navlit.com"
GuestName = "Guest"
AdminEmail = "admin@navlit.com"


class User(DBModel):
    email = CharField(null=False, unique=True)
    name = CharField(null=False)
    password_hash = CharField(null=False)
    role = CharField(null=False, default=Operator)
    actived = BooleanField(null=False, default=True)
    created = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'nav_user'

    @classmethod
    def user_exists(cls, email):
        insure_connect()
        try:
            e: User = cls.get((cls.email == email))
            return e
        except DoesNotExist:
            return None

    @classmethod
    def check_user_login(cls, email, hashed_password):
        insure_connect()
        try:
            e: User = cls.get((cls.email == email))
            if e.password_hash == hashed_password:
                return e
            else:
                return None
        except DoesNotExist:
            return None

    @classmethod
    def create_user(cls, email, name, hashed_password, role: str = Operator, actived: bool = False):
        insure_connect()
        cls.create(
            email=email,
            name=name,
            password_hash=hashed_password,
            role=role,
            actived=actived
        )
        return True

    @classmethod
    def update_user(cls, email, name: str = None, role: str = None, actived: bool = None):
        insure_connect()
        for user in User.select().where(User.email == email):
            if not_empty(name):
                user.name = name
            if not_empty(role):
                user.role = role
            if not_none(actived):
                logger.info(f"Update user {user.email} actived from {user.actived} to {actived}")
                user.actived = actived
            user.save()
        return True

    @classmethod
    def delete_user(cls, email: str):
        insure_connect()
        try:
            exists: User = cls.get(User.email == email)
            exists.delete_instance()
            return True
        except DoesNotExist:
            return False

    @classmethod
    def find_all(cls):
        insure_connect()
        return list(cls.select())

    @classmethod
    def find_user_email_to_name_map(cls):
        insure_connect()
        email_to_name_map = {u.email: u.name for u in cls.select()}
        email_to_name_map[GuestEmail] = GuestName
        return email_to_name_map

    @classmethod
    def find_user_count(cls):
        insure_connect()
        return cls.select().count()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def validate_password(password):
    return len(password) >= 8


with suppress(Exception):
    User.create_table()
    if User.select().count() == 0:
        logger.info("User initiate admin...")
        User.create_user(AdminEmail, "Admin", hash_password("admin@123"), role=Admin, actived=True)
