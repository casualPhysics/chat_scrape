import pytest
import requests

from endpoints_configs import ENDPOINT_CONFIGS


class EndPointTester(object):

    def __init__(self, endpoint: str, data: dict):
        self.endpoint = endpoint,
        self.data = data

    def call_request(self):
        return requests.put(self.endpoint, self.data)

    def generate_test_data(self, prompter, responder, text):
        return


def pytest_addoption(parser):
    parser.addoption(
        "--endpoint",
        action="store", default="LOCAL",
        help="my option: LOCAL or GLCOUD",
        choices=('LOCAL', 'GCLOUD')
    )


@pytest.fixture
def endpoint(request):
    return request.config.getoption("--endpoint")


@pytest.fixture
def endpoint(request):
    return request.config.getoption("--endpoint")


def test_endpoint(json_data, endpoint):
    print(endpoint)
    req = requests.put(ENDPOINT_CONFIGS[endpoint], json=json_data)
    return req


if __name__=="__main__":
    header = {'Authorization': 'Bearer ya29.a0Aa4xrXMTVpZansQneQf-kiScMsSjHJ06uvqiwXrXtrQHeeiCmThq4WY9rW6UVWpLmXLacp2B32Ji-OEOONuYiCcmBFSKgGC0Hp2qNNz86Tje5OetW18yB1YRgmhDO7yQSzxB5DDzi0AZCLaPS46yluJn83yfigaCgYKATASARESFQEjDvL9KxSiVznsHCoouHZ5KkCIqw0165'}
    txt = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages?q=in:sent after:2014/01/01 before:2014/02/01', headers = header)
    print(txt)