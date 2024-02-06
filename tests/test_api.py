import sys
from os.path import dirname, abspath

import pytest
from fastapi.testclient import TestClient

project_root = dirname(dirname(abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app, configure_api_routing

client = TestClient(app)
configure_api_routing()


USE_CASE = "bps"


@pytest.mark.skip(reason="adjust to use case")
def test_doc():
    response_ui = client.get(f"/{USE_CASE}")
    assert response_ui.status_code == 200, "Unexpected status code: {}".format(
        response_ui.status_code
    )
    assert (
        response_ui.headers["content-type"] == "text/html; charset=utf-8"
    ), "Content type is not as expected"
    assert (
        '<script type="text/hyperscript">' in response_ui.text
        or '<script type="text/javascript">' in response_ui.text
    ), "Script tags not found in response"


@pytest.mark.skip(reason="adjust to use case")
def test_config():
    response_ui = client.get(f"/{USE_CASE}/config")
    assert response_ui.status_code == 200, "Unexpected status code: {}".format(
        response_ui.status_code
    )
    assert (
        response_ui.headers["content-type"] == "text/html; charset=utf-8"
    ), "Content type is not as expected"
    assert "def submit()" in response_ui.text, "No submit function found"


@pytest.mark.skip(reason="adjust to use case")
def test_solution():
    response_ui = client.get(f"/{USE_CASE}/solution")
    assert response_ui.status_code == 200, "Unexpected status code: {}".format(
        response_ui.status_code
    )
    assert (
        response_ui.headers["content-type"] == "text/html; charset=utf-8"
    ), "Content type is not as expected"
    assert (
        '<script type="text/hyperscript">' in response_ui.text
        or '<script type="text/javascript">' in response_ui.text
    ), "Script tags not found in response"
