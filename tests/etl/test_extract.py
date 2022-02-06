import pytest
from etl.extract import get_all_columns, generate_blank_df, get_participant_data
from tests.etl.version_constants import V5

import pandas as pd

class TestCreateDataFrame:
    def test_get_all_columns_v5(self):
        cols = get_all_columns()
        expected_cols_v5 = V5

        assert cols == expected_cols_v5

    def test_generate_blank_df(self):
        expected_df = pd.DataFrame(columns=V5)
        got_df = generate_blank_df()
        
        pd.testing.assert_frame_equal(got_df, expected_df)

class TestGets:
    def test_participant_data(self):
        test_dict = {"level": 1,
                     "placement": 7,
                     "puuid": "a2isainasi2",
                     "other atributes": 123,
                     "test at": "maisn"}
        
        expected_dict ={"level": 1,
                        "placement": 7,
                        "puuid": "a2isainasi2",}
        
        got_dict = get_participant_data(test_dict)
        assert got_dict == expected_dict