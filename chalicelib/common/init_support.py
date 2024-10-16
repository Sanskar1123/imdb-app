from pymongo import ASCENDING, DESCENDING

from chalicelib.common import log_support
from chalicelib.common.mongo_collections import Mongo, DB_NAME, MOVIES_DATA_COLLECTION


def init_mongo_collection():
    try:
        indexes_to_create = [
            # ([("release_date", DESCENDING)], "release_date_index"),
            # ([("vote_average", DESCENDING)], "ratings_index"),
            # ([("languages", ASCENDING), ("release_date", DESCENDING)], "language_release_date_index"),
            ([("release_year", DESCENDING)], "release_year_index"),
            ([("languages", ASCENDING)], "languages_index"),
            ([("languages", ASCENDING), ("vote_average", DESCENDING)], "language_ratings_index"),
            ([("languages", ASCENDING), ("release_date", DESCENDING), ("vote_average", DESCENDING)], "language_release_date_ratings_index"),
        ]

        existing_indexes = list(mongo.get_indexes(MOVIES_DATA_COLLECTION))

        for index_fields, index_name in indexes_to_create:
            index_key = dict(index_fields)

            # Checking if the index already exists
            index_exists = False
            for existing_index in existing_indexes:
                if existing_index["key"] == index_key and existing_index.get("name") == index_name:
                    index_exists = True
                    log_support.console_log(f"Index '{index_name}' with fields {index_fields} already exists.")
                    break

            # If the index does not exist, create it
            if not index_exists:
                log_support.console_log(f"Index '{index_name}' with fields {index_fields} does not exist.")
                created_index = mongo.create_index(MOVIES_DATA_COLLECTION, fields=index_fields, name=index_name)
                log_support.console_log(f"Index '{created_index}' created.")

    except Exception as err:
        log_support.console_log(f"Exception while initialising mongodb: {str(err)}")


mongo = Mongo(DB_NAME)
init_mongo_collection()
