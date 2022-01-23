from dataclasses import dataclass, field
from importlib.metadata import metadata
import pandas as pd

from dotenv import dotenv_values
from typing import List, Any, Dict

from scrape.tft import TFTScraper
from etl.version_five import *

CONFIG = dotenv_values(".env")
API_KEY = CONFIG["KEY"]


def get_all_columns() -> List[str]:
    columns = COLUMNS.copy()
    columns.extend(NAME_TRAITS)
    columns.extend(NAME_UNITS)
    columns.extend(TIER_UNITS)
    return columns


def generate_blank_df() -> pd.DataFrame:
    columns = get_all_columns()

    return pd.DataFrame(columns=columns)


from typing import List, Any, Dict


def get_traits(list_traits: List[dict]) -> dict:
    trait = {}

    for dic in list_traits:
        name = dic["name"].split("_")[-1]
        trait[name] = dic["tier_total"]

    return trait


def get_units(list_units: List[dict]) -> dict:
    units = {}

    for dic in list_units:
        name = dic["character_id"].split("_")[-1]
        units[name] = dic["tier"]

    return units


def get_participant_data(participant: Dict[Any, Any]) -> Dict[Any, Any]:

    participant_dict = {}
    participant_dict["level"] = participant["level"]
    participant_dict["placement"] = participant["placement"]
    participant_dict["puuid"] = participant["puuid"]

    return participant_dict


def get_metadata_details(match_details: Dict[Any, Any]) -> Dict[Any, Any]:

    try:
        match_dict = match_details.metadata

    except:
        raise ValueError("No metadata in match_details")

    data_details = {}
    data_details["match_id"] = match_dict["match_id"]
    data_details["data_version"] = match_dict["data_version"]
    return data_details


def get_participant_units(participant: Dict[Any, Any]) -> Dict[Any, Any]:

    participant_units = {}
    participant_units["traits"] = get_traits(participant["traits"])
    participant_units["units"] = get_units(participant["units"])

    return participant_units


def data_from_summoner_name(name: str, count: int = None) -> pd.DataFrame:
    watcher = TFTScraper(api_key=API_KEY)
    match_history = watcher.get_match_history_summoner_name(name, count)
    df = generate_blank_df()

    for match_id in match_history:
        match_details = watcher.get_match_details_from_id(match_id)
        data_details = get_metadata_details(match_details)

        columns = df.columns

        for player in match_details.info["participants"]:

            aux_df = pd.DataFrame(columns=columns, index=[0])

            # Participant has the overall data for the player
            participant = get_participant_data(player)
            participant.update(data_details)

            for key, values in participant.items():
                aux_df.loc[0, key] = values

            participant_units = get_participant_units(player)

            # Add traits to dataframe
            name_traits = NAME_TRAITS.copy()

            for trait in name_traits:
                if trait in list(participant_units["traits"].keys()):
                    aux_df.loc[0, trait] = participant_units["traits"][trait]

            # Add units and tier to dataframe
            name_units = [
                name
                for name in columns
                if "unit" in name.split("_") and len(name.split("_")) == 2
            ]
            tier_units = [name for name in columns if "tier" in name.split("_")]

            for index, (name, tier) in enumerate(participant_units["units"].items()):
                aux_df.loc[0, name_units[index]] = name
                aux_df.loc[0, tier_units[index]] = tier

            df = df.append(aux_df, ignore_index=True)

    return df
