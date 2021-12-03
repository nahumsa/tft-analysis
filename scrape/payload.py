import requests
import json


class Payload:
    def __init__(self, j):
        self.__dict__ = json.loads(j)

    def __repr__(self) -> str:
        out_string = ""

        for key, value in self.__dict__.items():
            string = f"{key} = {value}"
            out_string += string + "\n"

        return out_string


class ResponseError(Exception):
    """Exception raised for errors in the response."""

    pass


def get_payload(response: requests.models.Response) -> Payload:
    """Generates a python object with the payload of the response of
    the request.

    Args:
        response (requests.models.Response): Response of the request.

    Raises:
        ResponseError: Error when the status code is not 200.

    Returns:
        Payload: Python object with the payolad of the request.
    """

    if response.status_code == 200:
        payload = Payload(response.text)
        return payload

    else:
        raise ResponseError(f"error occured with status code: {response.status_code}")
