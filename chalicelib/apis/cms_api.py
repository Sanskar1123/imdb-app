import json
import os

from chalice import Blueprint, Response
from chalicelib.common import cors_support, log_support
from chalicelib.support import cms_api_support


cms_api = Blueprint(__name__)
use_api_key = "True"
no_api_key = False


@cms_api.route('/api/upload/movies/csv', methods=['POST'], cors=cors_support.cors_config,
               content_types=['text/csv', 'application/csv'])
def upload_csv():
    """
        API to upload a csv file containing movies data.
    """
    try:
        body = cms_api.current_request.raw_body

        if not body:
            raise Exception("No file uploaded")
        max_size = int(os.getenv("MAX_CSV_FILE_SIZE_IN_MB", 1e2))  # 100 mb by default
        if len(body) > (max_size*1e6):
            raise Exception(f"File size should be less than {max_size}MB")

        response_message = cms_api_support.upload_csv_data(body)

        return Response(status_code=200, body={"message": response_message})
    except Exception as err:
        log_support.console_log(f"Exception @upload_csv: {str(err)}")
        return Response(status_code=502, body={"error": f"Exception @upload_csv: {str(err)}"})


@cms_api.route('/api/fetch/movies', methods=['POST'], cors=cors_support.cors_config)
def fetch_movies():
    """
    API to get a list of movies with pagination, filtering, and sorting.
    """
    try:
        request_payload = json.loads(cms_api.current_request.raw_body.decode())
        filter_params = request_payload.get('filter_params', {})
        sort_params = request_payload.get('sort_params', {})
        page_num = request_payload.get('page', 1)
        size_param = request_payload.get('size', 20)

        # Fetch movies using the utility function
        result = cms_api_support.fetch_movies(filter_params, sort_params, page_num, size_param)
        message = "Data fetched successfully" if len(result) > 0 else "No movie data found with the applied filter"
        response_body = ({"message": message, "data": result})

        return Response(status_code=200, body=response_body)
    except Exception as err:
        log_support.console_log(f"Exception @fetch_movies: {str(err)}")
        return Response(status_code=502, body={"error": f"Exception @fetch_movies: {str(err)}"})

