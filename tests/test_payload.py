import json
from scrape.payload import Payload


def test_payload():
    test_json = {}
    test_json["test"] = "ok"
    test_json["test2"] = "ok2"

    dump = json.dumps(test_json)

    assert Payload(dump).__dict__ == test_json
