import streamlit as st

from etl.extract import data_from_summoner_name
from visualization.most_common import plot_most_common_units, plot_most_common_traits
import matplotlib.pyplot as plt

st.set_page_config(page_title="TFT Analysis",
                   layout="wide")

col1, col2, col3 = st.columns(3)

# Put in the center
with col2:
    summoner_name = st.text_input("Summoner Name")

if summoner_name:
    
    col1, col2 = st.columns(2)
    df = data_from_summoner_name(summoner_name, 10)
    
    with col1:
        fig, ax = plt.subplots(1, 2, figsize=(8, 6)) 
        plot_most_common_units(df, ax[0])
        plot_most_common_traits(df, ax[1])
        
        # TODO: Slider
        st.markdown("<h3 style='text-align: center;'>All players</h3>", unsafe_allow_html=True)
        st.pyplot(fig)
    
    with col2:
        # TODO: Placement Selector
        top_players = df[df["placement"].isin([1, 2, 3])]
        
        # TODO: Slider
        fig, ax = plt.subplots(1, 2, figsize=(8, 6)) 
        plot_most_common_units(top_players, ax[0])
        plot_most_common_traits(top_players, ax[1])
        
        st.markdown("<h3 style='text-align: center;'>Top 3 players in all matches</h3>", unsafe_allow_html=True)
        st.pyplot(fig)