import datetime
from contextlib import suppress
from datetime import datetime as dt

from peewee import CharField, DateTimeField, fn
from models import DBModel, insure_connect
from models.user import GuestName


class Trend(DBModel):
    website_category = CharField(null=False)
    website_name = CharField(null=False)
    user_email = CharField(null=True)
    created = DateTimeField(default=dt.now())

    class Meta:
        db_table = 'nav_trend'

    @classmethod
    def create_trend(cls, website_category: str, website_name: str, user_email: str = None, user_ip: str = None):
        insure_connect()
        user_identify = user_email
        if user_identify is None:
            user_identify = f"{GuestName}@{user_ip}" if user_ip is not None else GuestName
        cls.create(
            website_category=website_category,
            website_name=website_name,
            user_email=user_identify,
        )
        return True

    @classmethod
    def find_weekly_trends(cls):
        insure_connect()
        return list(cls.select().where(cls.created >= dt.now() - datetime.timedelta(days=7)))

    @classmethod
    def find_totally_count(cls):
        insure_connect()
        return cls.select().count()

    @classmethod
    def find_weekly_count(cls):
        insure_connect()
        return cls.select().where(cls.created >= dt.now() - datetime.timedelta(days=7)).count()

    @classmethod
    def find_daily_count(cls):
        insure_connect()
        return cls.select().where(cls.created >= dt.now() - datetime.timedelta(days=1)).count()

    @classmethod
    def find_weekly_website_top10(cls):
        insure_connect()
        query = (cls.select(cls.website_name, fn.COUNT(cls.website_name).alias('count'))
                 .group_by(cls.website_name)
                 .where(cls.created >= dt.now() - datetime.timedelta(days=7))
                 .order_by(fn.COUNT(cls.website_name).desc())
                 .limit(10))

        websits = list()
        counts = list()
        for row in query.dicts():
            websits.append(row['website_name'])
            counts.append(row['count'])

        return {
            'websits': websits,
            'counts': counts
        }

    @classmethod
    def find_user_top10(cls):
        insure_connect()
        query = (cls.select(cls.user_email, fn.COUNT(cls.user_email).alias('count'))
                 .group_by(cls.user_email)
                 .where(cls.user_email.is_null(False))
                 .order_by(fn.COUNT(cls.user_email).desc())
                 .limit(10))

        emails = list()
        counts = list()
        for row in query.dicts():
            emails.append(row['user_email'])
            counts.append(row['count'])

        return {
            'emails': emails,
            'counts': counts
        }


with suppress(Exception):
    Trend.create_table()
