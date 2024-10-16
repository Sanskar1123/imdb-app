import ast
import pandas as pd
from io import StringIO
from chalice import BadRequestError

from chalicelib.common import log_support
from chalicelib.common.init_support import mongo
from chalicelib.common.mongo_collections import MOVIES_DATA_COLLECTION


def upload_csv_data(raw_body):
    """
    Process the raw CSV data from the request body,
    validate headers, and insert data into MongoDB.

    Parameters:
        raw_body (bytes): The raw body of the CSV request.

    Returns:
        str: Success message after processing the data.

    Raises:
        BadRequestError: If headers are invalid or if any other issue occurs.
    """
    expected_headers = [
        "budget", "homepage", "original_language", "original_title",
        "overview", "release_date", "revenue", "runtime",
        "status", "title", "vote_average", "vote_count",
        "production_company_id", "genre_id", "languages"
    ]
    try:

        # Decode raw body
        body = raw_body.decode('utf-8')

        # Read CSV into a DataFrame
        df = pd.read_csv(StringIO(body))

        # Validate headers
        if list(df.columns) != expected_headers:
            raise BadRequestError(f"Invalid CSV headers. Expected: {str(expected_headers)}")

        if 'release_date' in df.columns:
            df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

        # Converting languages column to array type
        if 'languages' in df.columns:
            df['languages'] = df['languages'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

        # Convert DataFrame to a list of dictionaries
        documents = df.to_dict(orient='records')  # Convert to list of dicts for MongoDB

        # Perform bulk insert, using insert_many to ensure atomic operation
        if documents:
            mongo.insert_many_document(MOVIES_DATA_COLLECTION, documents)
        else:
            raise pd.errors.EmptyDataError(f"No data found in the CSV")

        return "Data uploaded successfully"

    except UnicodeDecodeError:
        raise BadRequestError("Error parsing the file. Please ensure it is well-formed CSV file.")
    except pd.errors.EmptyDataError:
        raise BadRequestError("No data found in the CSV.")
    except pd.errors.ParserError:
        raise BadRequestError("Error parsing the file. Please ensure it is well-formed CSV file.")
    except BadRequestError as err:
        raise BadRequestError(str(err))
    except Exception as err:
        raise Exception(f"{str(err)}")
    return False


def validate_fetch_params(filter_params, sort_params, page_num, size_param):
    """
        Validate and parse the payload to filter data,
        and fetch data from MongoDB.

        Parameters:
            :param filter_params: Filter data based on these parameters
            :param sort_params: Sort data based on these parameters
            :param page_num: Page number
            :param size_param: Size of each page

        Returns:
            tuple: Parsed payload params.
    """
    filter_keys_to_keep = {"languages", "release_year"}
    sort_keys_to_keep = {"ratings", "vote_average", "release_date", "release_year"}

    restricted_sort_params = {key: sort_params[key] for key in sort_keys_to_keep if key in sort_params}
    for key, value in restricted_sort_params.items():
        if value not in {-1, 1}:
            raise BadRequestError("Sort params only accept -1 (descending) or 1 (ascending) as value")
    sort_order_params = [(key, value) for key, value in restricted_sort_params.items()]

    restricted_filter_params = {key: filter_params[key] for key in filter_keys_to_keep if key in filter_params}

    total_doc_count = mongo.count_documents_by_filter(MOVIES_DATA_COLLECTION, restricted_filter_params)
    if total_doc_count == 0:
        return list()
    max_page = (total_doc_count + size_param - 1) // size_param  # Calculate maximum number of pages

    # Ensuring page_num does not exceed max_page
    if page_num > max_page or page_num <= 0:
        raise BadRequestError(f"Requested page {page_num} doesn't exist. "
                              f"Please enter page number between 1 and maximum available pages {max_page}")
    start_index = (page_num - 1) * size_param

    return restricted_filter_params, sort_order_params, start_index


def fetch_movies(filter_params, sort_params, page_num, size_param):
    """
    Process the payload from the request body to filter data,
    and fetch data from MongoDB.

    Parameters:
        :param filter_params: Filter data based on these parameters
        :param sort_params: Sort data based on these parameters
        :param page_num: Page number
        :param size_param: Size of each page

    Returns:
        list: Movies data from MongoDB.
    """
    try:

        filter_params, sort_params, start_index = validate_fetch_params(filter_params, sort_params,
                                                                        page_num, size_param)

        records = mongo.fetch_records_with_query(MOVIES_DATA_COLLECTION, filter_params=filter_params,
                                                 sort_params=sort_params, start_index=start_index,
                                                 size=size_param, projection_query={'_id': False})
        log_support.console_log("Fetched required records")
        return records
    except BadRequestError as err:
        raise BadRequestError(str(err))
    except Exception as err:
        raise Exception(f"An error occurred while fetching filtered movies data: {str(err)}")
    return False
