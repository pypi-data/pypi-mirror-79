from pymongo import MongoClient, DESCENDING

from fdbk import DBConnection
from fdbk.utils import (
    generate_data_entry,
    generate_topic_dict,
    generate_topic_response,
    generate_topics_list,
    timestamp_as_str)
from fdbk.utils.messages import *


PROJECTION = dict(_id=0)


class MongoDbConnection(DBConnection):
    def __init__(
            self,
            mongo_url,
            db_name="fdbk",
            username=None,
            password=None,
            auth_source="admin"):
        self._client = MongoClient(mongo_url)
        self._db = self._get_db(db_name, username, password, auth_source)

    def _get_db(self, db_name, username, password, auth_source):
        database = self._client[db_name]
        if username and password:
            database.authenticate(username, password, source=auth_source)
        return database

    def add_topic(self, name, overwrite=False, **kwargs):
        topic_d = generate_topic_dict(name, add_id=True, **kwargs)
        self.validate_template(topic_d)

        try:
            self.get_topic(topic_d.get('id'))
        except KeyError:
            self._db["topics"].insert_one(topic_d)
        else:
            if not overwrite:
                raise KeyError(duplicate_topic_id(topic_d["id"]))
            self._db["topics"].replace_one({"id": topic_d.get('id')}, topic_d)

        return topic_d["id"]

    def add_data(self, topic_id, values, overwrite=False):
        topic_d = self.get_topic(topic_id)
        fields = topic_d["fields"]

        if topic_d.get('type') != 'topic':
            raise AssertionError('Can not add data to template.')

        data = generate_data_entry(
            topic_id, fields, values, convert_timestamps=True)
        search_d = {"topic_id": topic_id, 'timestamp': data["timestamp"]}
        exists = self._db["data"].find_one(search_d)

        if not exists:
            self._db["data"].insert_one(data)
        else:
            if not overwrite:
                raise AssertionError(
                    duplicate_timestamp(
                        topic_d, data["timestamp"]))
            self._db["data"].replace_one(search_d, data)

        return data["timestamp"]

    def get_topics_without_templates(self, type_=None, template=None):
        search_d = {}
        if type_:
            search_d["type"] = type_
        if template:
            search_d["template"] = template

        topics = self._db["topics"].find(search_d, PROJECTION)
        return generate_topics_list(topics)

    def get_topic_without_templates(self, topic_id):
        topic = self._db["topics"].find_one({"id": topic_id}, PROJECTION)
        if not topic:
            raise KeyError(topic_not_found(topic_id))

        return generate_topic_response(topic)

    @staticmethod
    def _add_timestamp_query(query):
        if not query.get("timestamp"):
            query["timestamp"] = {}

    def get_data(self, topic_id, since=None, until=None, limit=None):
        if not limit:
            limit = 500

        # Check that topic exists
        self.get_topic(topic_id)

        search_d = {
            "topic_id": topic_id,
        }

        if since:
            self._add_timestamp_query(search_d)
            search_d["timestamp"]["$gte"] = timestamp_as_str(since)
        if until:
            self._add_timestamp_query(search_d)
            search_d["timestamp"]["$lte"] = timestamp_as_str(until)

        data = list(
            self._db["data"].find(
                search_d, PROJECTION, sort=[
                    ('timestamp', DESCENDING)], limit=limit))
        data.reverse()
        return data
