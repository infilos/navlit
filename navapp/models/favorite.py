from contextlib import suppress
from datetime import datetime

from peewee import DoesNotExist, CharField, DateTimeField, IntegerField, fn

from models import DBModel, insure_connect
from models.website import Website


class Favorite(DBModel):
    user_email = CharField(null=False)
    website_id = IntegerField(null=False)
    created = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'nav_favorite'

    @classmethod
    def check_exists(cls, user_email: str, website_id: int):
        insure_connect()
        try:
            e: Favorite = cls.get((cls.user_email == user_email and cls.website_id == website_id))
            return True
        except DoesNotExist:
            return False

    @classmethod
    def create_favorite(cls, user_email: str, website_id: int):
        insure_connect()
        cls.create(
            user_email=user_email,
            website_id=website_id,
        )
        return True

    @classmethod
    def delete_favorite(cls, user_email: str, website_id: int):
        insure_connect()
        try:
            exists: Favorite = cls.get((cls.user_email == user_email and cls.website_id == website_id))
            exists.delete_instance()
            return True
        except DoesNotExist:
            return False

    @classmethod
    def find_user_favorites(cls, user_email: str):
        insure_connect()
        return list(cls.select().where(cls.user_email == user_email))

    @classmethod
    def find_favorite_top10(cls):
        insure_connect()
        query = (cls.select(cls.website_id, fn.COUNT(cls.website_id).alias('count'))
                 .group_by(cls.website_id)
                 .order_by(fn.COUNT(cls.website_id).desc())
                 .limit(10))

        websits = list()
        counts = list()
        for row in query.dicts():
            websits.append(row['website_id'])
            counts.append(row['count'])

        id_to_name = dict((w.id, w.name) for w in Website.find_websites_in_ids(websits))

        return {
            'websits': [id_to_name[x] for x in websits],
            'counts': counts
        }


with suppress(Exception):
    Favorite.create_table()
