from chalice.test import Client
from tests import env_variables

env_variables.add_os_variables()
import app


def test_health_check():
    with Client(app.app) as client:
        response = client.http.get(
            '/api/health_check'
        )
        assert response.status_code == 200
