from peewee import Model
from peewee import SqliteDatabase
from playhouse.shortcuts import ReconnectMixin
from utils import build_conf_dir


class ReconnectSqliteDatabase(ReconnectMixin, SqliteDatabase):
    pass


path = f"sqlite://{build_conf_dir()}/navlit.db"
db = ReconnectSqliteDatabase(f"{build_conf_dir()}/navlit.db")


class DBModel(Model):
    class Meta:
        database = db


def insure_connect():
    if db.is_closed():
        db.connect()
