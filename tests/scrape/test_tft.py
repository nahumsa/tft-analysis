import json
import responses
import requests
import pytest

from scrape.tft import TFTScraper

api_key = "1111"


@responses.activate
def test_from_summoner_name():
    expected_json = {
        "id": "123131",
        "accountId": "buifudiofn1iu34b1",
        "puuid": "test",
        "name": "test",
        "profileIconId": 100,
        "revisionDate": 68746847687,
        "summonerLevel": 544,
    }
    responses.add(
        responses.GET,
        f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/test?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.from_summoner_name("test").__dict__
    assert got == expected_json


@responses.activate
def test_get_match_history_puuid_count():
    expected_json = [
        "BR1_2412716601",
    ] * 30

    responses.add(
        responses.GET,
        f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/1232142/ids?api_key={api_key}&count=30",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.get_match_history_puuid("1232142", count=30)
    assert got == expected_json


@responses.activate
def test_get_match_history_puuid_default():
    expected_json = ["BR1_2407123803"] * 20

    responses.add(
        responses.GET,
        f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/1232142/ids?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.get_match_history_puuid("1232142")
    assert got == expected_json


@responses.activate
def test_get_match_history_puuid_default():
    expected_json = {
        "id": "123131",
        "accountId": "buifudiofn1iu34b1",
        "puuid": "test",
        "name": "test",
        "profileIconId": 100,
        "revisionDate": 68746847687,
        "summonerLevel": 544,
    }

    responses.add(
        responses.GET,
        f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/test?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    expected_json = ["BR1_2407123803"] * 20
    responses.add(
        responses.GET,
        f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/test/ids?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.get_match_history_summoner_name("test")
    assert got == expected_json


@responses.activate
def test_get_match_details_from_id():
    expected_json = {
        "metadata": {},
        "info": {},
    }

    responses.add(
        responses.GET,
        f"https://americas.api.riotgames.com/tft/match/v1/matches/123?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.get_match_details_from_id("123").__dict__
    assert got == expected_json


@responses.activate
def test_get_gm_summoner_name_list():
    expected_json = {
        "entries": [
            {
                "summonerName": "test",
            }
            for _ in range(10)
        ]
    }

    expected_list = ["test"] * 10

    responses.add(
        responses.GET,
        f"https://br1.api.riotgames.com/tft/league/v1/challenger?api_key={api_key}",
        json=expected_json,
        status=200,
    )

    watcher = TFTScraper(api_key=api_key)
    got = watcher.get_gm_summoner_name_list()
    assert got == expected_list
