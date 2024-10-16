import os
import urllib.parse
from pymongo import MongoClient


DB_NAME = 'imdb'
MOVIES_DATA_COLLECTION = "movies_data"


class Mongo:
    def __init__(self, db_name=None):
        """
        :param db_name: The database name in mongo db.
        """
        if db_name is None:
            raise ValueError("DB Name is missing in constructor params.")
        self.db_name = db_name
        self.mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.mongo_password = os.getenv("MONGODB_PASSWORD")
        self.client = self.get_client()
        self.http_timeout = 60

    def get_client(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = str(self.mongo_connection_string).replace("{password}",
                                                                      urllib.parse.quote(self.mongo_password))
        client = MongoClient(CONNECTION_STRING)
        return client

    def get_collection(self, collection_name):
        """
        :param collection_name: returns the collection
        :return:
        """
        client = self.client
        return client[self.db_name][collection_name]

    def get_indexes(self, collection_name):
        """
        :param collection_name: The name of the collection
        :return: index list
        """
        collection = self.get_collection(collection_name)
        indexes = collection.list_indexes()

        return indexes

    def create_index(self, collection_name, fields, name):
        """
        :param collection_name: The name of the collection in which the index will be created
        :param fields: Index fields that will be created
        :param name: Name of the index that will be created
        desc: create indexes on collections to improve the performance of queries.
        :return: index name
        """
        collection = self.get_collection(collection_name)
        category_index = collection.create_index(fields, name=name)
        return category_index

    def insert_many_document(self, collection_name, documents):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param documents: Document that will be inserted in the collection
        :return: Generic PyMongo response for "insert_many"
        """
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)

    def insert_document(self, collection_name, document):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param document: Document that will be inserted in the collection
        :return:
        """
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def fetch_records_with_query(self, collection_name, filter_params=None, sort_params=None, start_index=None,
                                 size=None, projection_query=None):
        """
        :param collection_name:
        :param filter_params:
        :param sort_params:
        :param start_index:
        :param size:
        :param projection_query:
        :return: List of records filtered through pagination i.e.e skip and limit with fields mentioned in projection query.
        """
        if projection_query is None:
            projection_query = {}
        collection = self.get_collection(collection_name)
        args = []
        kwargs = {}
        if filter_params:
            args.append(filter_params)
        if projection_query:
            kwargs.update(projection=projection_query)

        query_result = collection.find(*args, **kwargs)
        if sort_params:
            query_result = query_result.sort(sort_params)
        if start_index:
            query_result = query_result.skip(start_index)
        if size:
            query_result = query_result.limit(size)
        records = list(query_result)
        return records

    def count_documents_by_filter(self, collection_name, query):
        """
        :param collection_name:
        :param query:
        :return: returns num of records that matched the query.
        """
        collection = self.get_collection(collection_name)
        return collection.count_documents(query)
