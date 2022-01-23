import requests
from dataclasses import dataclass
import json
from typing import List
from scrape.payload import get_payload, Payload


@dataclass
class TFTScraper:
    api_key: str

    def _send_request(self, url: str, count: int = None) -> requests.models.Response:
        url_request = f"{url}?api_key={self.api_key}"

        if count:
            url_request += f"&count={count}"

        return requests.get(url_request)

    def from_summoner_name(self, name: str) -> Payload:
        summonder_url = (
            f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}"
        )

        return get_payload(self._send_request(summonder_url))

    def get_match_history_puuid(self, puuid: str, count: int = None) -> List[dict]:
        match_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
        response = self._send_request(match_url, count=count)
        return json.loads(response.text)

    def get_match_history_summoner_name(
        self, name: str, count: int = None
    ) -> List[dict]:
        payload = self.from_summoner_name(name)
        return self.get_match_history_puuid(payload.puuid, count)

    def get_match_details_from_id(self, id: str) -> Payload:
        match_details_url = (
            f"https://americas.api.riotgames.com/tft/match/v1/matches/{id}"
        )
        return get_payload(self._send_request(match_details_url))

    def get_gm_summoner_name_list(self) -> List[str]:
        gm_url = f"https://br1.api.riotgames.com/tft/league/v1/challenger"
        payload = get_payload(self._send_request(gm_url))

        return [entries_dict["summonerName"] for entries_dict in payload.entries]
