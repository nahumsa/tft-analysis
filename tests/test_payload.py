import json
import responses
import requests
import pytest

from scrape.payload import Payload, get_payload, ResponseError

test_json = {}
test_json["test"] = "ok"
test_json["test2"] = "ok2"
dump = json.dumps(test_json)


def test_payload_dict():
    assert Payload(dump).__dict__ == test_json


def test_payload_repr():
    expected = "test = ok\ntest2 = ok2\n"
    assert repr(Payload(dump)) == expected


@responses.activate
def test_get_payload_accept():
    responses.add(responses.GET, "http://test.com/api/", json=test_json, status=200)

    resp = requests.get("http://test.com/api/")
    assert get_payload(resp).__dict__ == test_json


@responses.activate
def test_get_payload_response_error():
    responses.add(responses.GET, "http://test.com/api/", json=test_json, status=401)

    resp = requests.get("http://test.com/api/")
    with pytest.raises(ResponseError):
        get_payload(resp)
