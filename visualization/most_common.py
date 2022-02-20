import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


from etl.transform import get_most_common_data, get_clean_full_data

def plot_most_common_units(df: pd.DataFrame, ax) -> None:
    
    _, all_units, _ = get_clean_full_data(df)

    df_units = get_most_common_data(all_units, name="unit")
    df_units["Percentage"] = df_units["quantity"] / df.shape[0]
    
    # fix 10 most common units
    n_units = 10
    df_units = df_units.iloc[:n_units, :]
    
    sns.barplot(y="Percentage",
                x="unit",
                color="blue",
                data=df_units,
                ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation = 90,
                       fontsize=8)
    ax.set_ylim([0., 1.])
    
def plot_most_common_traits(df: pd.DataFrame, ax) -> None:
    
    _, _, all_traits = get_clean_full_data(df)

    df_traits = get_most_common_data(all_traits, name="traits")
    df_traits["quantity"] = df_traits["quantity"] / df.shape[0]
    
    ax = sns.barplot(y="quantity",
                    x="traits",
                    color="blue",
                    data=df_traits)

    ax.set_ylabel("Level per player")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=8)
    ax.set_ylim([0., 5.])