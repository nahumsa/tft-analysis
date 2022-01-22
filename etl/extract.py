from dataclasses import dataclass, field
from importlib.metadata import metadata
import pandas as pd

from dotenv import dotenv_values
from typing import List
from scrape.tft import TFTScraper

CONFIG = dotenv_values(".env")
API_KEY = CONFIG["KEY"]    

def generate_blank_df() -> pd.DataFrame:
    columns = ["match_id", "data_version", "level", "placement", "puuid"]

    name_traits = ["Arcanist", "Assassin", "Bodyguard", "Bruiser", "Challenger", "Colossus",
                "Enchanter", "Innovator", "Protector", "Scholar", "Sniper", "Transformer",
                "Twinshot",]
    name_traits = [f"trait_{name}" for name in name_traits]
    
    name_units = [f"unit_{i}" for i in range(9)]
    tier_units = [f"tier_unit_{i}" for i in range(9)]

    columns.extend(name_traits)
    columns.extend(name_units)
    columns.extend(tier_units)

    return pd.DataFrame(columns=columns)
    

def data_from_summoner_name(name: str, count: int) -> pd.DataFrame:
    watcher = TFTScraper(api_key=API_KEY)
    match_history = watcher.get_match_history_summoner_name(name)
    
