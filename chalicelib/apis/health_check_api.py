from chalice import Blueprint, Response

health_check_api = Blueprint(__name__)


@health_check_api.route('/api/health_check', methods=['GET'])
def health_check():
    """
        API to ensure that the service is running.
    """
    return Response(status_code=200, body={"status": "RUNNING"})
