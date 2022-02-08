import pandas as pd
from typing import Tuple, List, Dict
from collections import Counter 

from etl.version.v5 import COLUMNS


def get_most_common_data(data: List[Dict[str, int]], name: str) -> pd.DataFrame:
    """Extract the most common occurence in the data.

    Args:
        data (List[Dict[str, int]]): data to count
        name (str): name for the column of the dataframe

    Returns:
        pd.DataFrame: Counter for the data.
    """
    common_units = Counter()

    for value in data:
        common_units += Counter(**value)

    return pd.DataFrame(common_units.most_common(), columns=[name, "quantity"])


def get_name_tier(entry: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """Return two pd.Series for the name of units and the tier of each
    unit.

    Args:
        entry (pd.Series): Cleaned entry that you want to extract.

    Returns:
        pd.Series: Name series
        pd.Series: Tier series
    """
    columns = list(entry.index)
    name_units = [
                    name
                    for name in columns
                    if "unit" in name.split("_") and len(name.split("_")) == 2
    ]
    tier_units = [name for name in columns if "tier" in name.split("_")]
    
    name_series = entry[name_units]
    tier_series = entry[tier_units]
    
    name_units.extend(tier_units)
    entry.drop(labels=name_units, inplace=True)
    
    return name_series, tier_series

def get_clean_match_data(df: pd.DataFrame, match_id: str) -> Tuple[list, list, list]:
    """Generate lists for player info, units, and traits.

    Args:
        df (pd.DataFrame): dataframe
        match_id (str): identifier of the match

    Returns:
        list: player(s) information for the match
        list: units information for the match
        list: traits information for the match
    """
    df_match = df[df.match_id == match_id]
    
    units = []
    player_info = []
    traits = []

    for _, row in df_match.iterrows():
        entry_clean = row.dropna()    

        # Extract level, puuid, and placement
        player_info.append({"level": entry_clean.level,
                            "puuid": entry_clean.puuid,
                            "placement":entry_clean.placement})    
        
        # Remove player info rows
        entry_clean.drop(labels=COLUMNS, inplace=True)
        
        # Get units data
        name_series, tier_series = get_name_tier(entry_clean)
        units.append({name_series[i]: tier_series[i] for i in range(len(name_series))})
        
        # Get traits data
        traits.append({trait: n for trait, n in entry_clean.iteritems()})

    return player_info, units, traits

def get_clean_full_data(df: pd.DataFrame) -> Tuple[list, list, list]:
    """Generate lists for player info, units, and traits for all matches
    in the dataframe.

    Args:
        df (pd.DataFrame): dataframe of matches
        match_id (str): identifier of the match

    Returns:
        list: player(s) information for the match
        list: units information for the match
        list: traits information for the match
    """
    all_player_info, all_units, all_traits = [], [], []
    
    unique_matches = list(set(df.match_id))
    
    for match_id in unique_matches:
        player_info, units, traits = get_clean_match_data(df, match_id)
        all_player_info.extend(player_info)
        all_units.extend(units)
        all_traits.extend(traits)
    
    return all_player_info, all_units, all_traits