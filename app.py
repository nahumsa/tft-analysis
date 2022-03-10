import streamlit as st

from etl.extract import data_from_summoner_name, puuid_from_name
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
    puuid = puuid_from_name(summoner_name)
    df = data_from_summoner_name(summoner_name, 10)
    
    with col1:
        fig, ax = plt.subplots(1, 2, figsize=(8, 6)) 
        plot_most_common_units(df, ax[0])
        plot_most_common_traits(df, ax[1])
        
        st.markdown("<h3 style='text-align: center;'>All players</h3>", unsafe_allow_html=True)
        st.pyplot(fig)
    
    with col2:
        placement = st.multiselect("Placements on the analysis", [i for i  in range(1, 7)])
        
        if placement:
            top_players = df[df["placement"].isin(placement)]
        
            fig, ax = plt.subplots(1, 2, figsize=(8, 6)) 
            plot_most_common_units(top_players, ax[0])
            plot_most_common_traits(top_players, ax[1])
            
            # Convert from int to string to display
            placement_str = [str(i) for i in placement]
            
            st.markdown(f"<h3 style='text-align: center;'>Statistics for {', '.join(placement_str)} place(s) in all matches</h3>", unsafe_allow_html=True)
            # Change the plots
            st.pyplot(fig)
            
    # TODO: filter matches using PUUID