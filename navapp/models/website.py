from contextlib import suppress
from datetime import datetime
from functools import reduce
from loguru import logger

from peewee import DoesNotExist, CharField, AutoField, BlobField, DateTimeField, BooleanField

from models import DBModel, insure_connect
from models.user import AdminEmail
from utils import not_empty


class Website(DBModel):
    id = AutoField(primary_key=True)
    category = CharField(null=False, index=True)
    name = CharField(null=False, index=True)
    descr = CharField(null=True, index=True)
    url = CharField(null=False, index=True)
    img_url = CharField(null=True)
    img_data = BlobField(null=True, default=None)
    actived = BooleanField(null=False, default=True)
    owner = CharField(null=False)
    creator = CharField(null=False)
    updater = CharField(null=False)
    created = DateTimeField(default=datetime.now())
    updated = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'nav_website'

    @classmethod
    def create_website(cls, category: str, name: str, url: str, creator: str, acvited: bool = True, descr: str = None, img_url: str = None, img_data: bytes = None):
        insure_connect()
        cls.create(
            category=category,
            name=name,
            descr=descr,
            url=url,
            img_url=img_url,
            img_data=img_data,
            actived=acvited,
            owner=creator,
            creator=creator,
            updater=creator,
        )
        return True

    @classmethod
    def update_website(cls, _id: int, updater: str, category: str = None, name: str = None, url: str = None, descr: str = None, actived: bool = None, owner: str = None, img_url: str = None, img_data: str = None):
        insure_connect()
        for website in Website.select().where(Website.id == _id):
            if not_empty(category):
                website.category = category
            if not_empty(name):
                website.name = name
            if not_empty(descr):
                website.descr = descr
            if not_empty(url):
                website.url = url
            if not_empty(img_url):
                website.img_url = img_url
            if img_data is not None:
                website.img_data = img_data
            if not_empty(owner):
                website.owner = owner
            if actived is not None:
                website.actived = actived

            website.updater = updater
            website.updated = datetime.now()
            website.save()
        return True

    @classmethod
    def delete_website(cls, _id: int):
        insure_connect()
        try:
            exists: Website = cls.get(Website.id == _id)
            exists.delete_instance()
            return True
        except DoesNotExist:
            return False

    @classmethod
    def find_all_websites(cls, keywrod: str = None, creator: str = None, actived: bool = None):
        insure_connect()
        conds = list()
        if not_empty(keywrod):
            conds.append(Website.category.contains(keywrod) |
                         Website.name.contains(keywrod) |
                         Website.descr.contains(keywrod) |
                         Website.url.contains(keywrod))
        if creator:
            conds.append(Website.creator == creator)
        if actived:
            conds.append(Website.actived == actived)
        if len(conds) > 0:
            return list(Website.select().where(reduce(lambda x, y: x & y, conds)))
        return list(Website.select())

    @classmethod
    def find_website_count(cls):
        insure_connect()
        return cls.select().count()

    @classmethod
    def find_category_count(cls):
        insure_connect()
        return cls.select(Website.category).distinct().count()

    @classmethod
    def find_websites_in_ids(cls, ids: list[int]):
        insure_connect()
        return list(Website.select().where(Website.id << ids))


with suppress(Exception):
    Website.create_table()
    logger.info(f"Website exists count: {Website.select().count()}")
    if Website.select().count() == 0:
        logger.info(f"Website initiate start...")
        Website.create_website("Search", "Bing", "https://bing.com", AdminEmail)
        Website.create_website("Search", "Bing", "https://bing.com", AdminEmail)
        Website.create_website("Search", "Bing", "https://bing.com", AdminEmail)
        Website.create_website("Search", "Google", "https://google.com", AdminEmail)
        Website.create_website("Search", "Google", "https://google.com", AdminEmail)
        Website.create_website("Search", "Google", "https://google.com", AdminEmail)
        Website.create_website("Code", "Github", "https://github.com", AdminEmail)
        Website.create_website("Code", "Github", "https://github.com", AdminEmail)
        Website.create_website("Code", "Github", "https://github.com", AdminEmail)
        Website.create_website("Code", "Gitlab", "https://gitlab.com", AdminEmail)
        Website.create_website("Code", "Gitlab", "https://gitlab.com", AdminEmail)
        Website.create_website("Video", "Youtube", "https://youtube.com", AdminEmail)
        Website.create_website("Video", "Bilibili", "https://bilibili.com", AdminEmail)
        Website.create_website("Video", "Bilibili", "https://bilibili.com", AdminEmail)
        Website.create_website("Tools", "JSON Diff", "https://json-diff.com", AdminEmail)
        Website.create_website("Tools", "Regex101", "https://regex101.com", AdminEmail)
        logger.info(f"Website initiate complete.")
