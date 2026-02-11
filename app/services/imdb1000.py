import json
import pandas as pd
from fastapi.responses import JSONResponse

def get_movie_stats(df:pd.DataFrame, col_name:str) -> pd.DataFrame:
    stats_df = df.groupby(col_name).agg(
        Movie_Count=pd.NamedAgg(column="Series_Title", aggfunc="count"),
        Total_Gross=pd.NamedAgg(column="Gross", aggfunc="sum"),
        Avg_Gross=pd.NamedAgg(column="Gross", aggfunc="mean"),
        Avg_IMDB_Rating=pd.NamedAgg(column="IMDB_Rating", aggfunc="mean"),
        Avg_Meta_score=pd.NamedAgg(column="Meta_score", aggfunc="mean"),
    ).reset_index()

    return stats_df

def get_actor_stats(df:pd.DataFrame, col_name:str) -> pd.DataFrame:
    df["isTopBilling"] = df["Billing"] == "Star1"
    df["isSecondBilling"] = df["Billing"] == "Star2"
    df["isOtherBilling"] = (df["Billing"]=="Star3") | (df["Billing"]=="Star4")

    stats_df = df.groupby(col_name).agg(
        Movie_Count=pd.NamedAgg(column="Series_Title",aggfunc="count"),
        Top_Billing=pd.NamedAgg(column="isTopBilling", aggfunc="sum"),
        Second_Billing=pd.NamedAgg(column="isSecondBilling", aggfunc="sum"),
        Other_Billing=pd.NamedAgg(column="isOtherBilling", aggfunc="sum"),
        Total_Gross=pd.NamedAgg(column="Gross", aggfunc="sum"),
        Avg_Gross=pd.NamedAgg(column="Gross", aggfunc="mean"),
        Avg_IMDB_Rating=pd.NamedAgg(column="IMDB_Rating", aggfunc="mean"),
        Avg_Meta_score=pd.NamedAgg(column="Meta_score", aggfunc="mean"),
    ).reset_index()

    return stats_df


class Imdb1000Service:
    def __init__(self, df: pd.DataFrame, limit = 100):
        self._df_full = df
        self._df = df.head(limit)

    @property
    def df(self):
        return self.df
    
    def imdb1000(self):
        return self
    
    def director(self, name, sort_by, sort_direction):
        if not name:
            stats_df = get_movie_stats(self._df_full, "Director")
            if sort_by:
                is_asc = sort_direction == "asc"
                stats_df = stats_df.sort_values(sort_by,ascending=is_asc)
            self._df = stats_df
        else:
            filter = self._df_full["Director"] == name
            self._df = self._df_full[filter]
        return self
    
    def actor(self, name, sort_by, sort_direction):
        keep_col = ["Series_Title","Released_Year","Runtime","Genre","IMDB_Rating","Overview","Meta_score","Director","No_of_Votes","Gross"]
        expanded_df = self._df_full.melt(id_vars=keep_col, value_vars=["Star1","Star2","Star3","Star4"], var_name="Billing", value_name="Actor")
        expanded_df['Billing'] = expanded_df['Billing'].astype("category")
        expanded_df['Actor'] = expanded_df['Actor'].astype("category")

        if not name:
            stats_df = get_actor_stats(expanded_df, "Actor")
            if sort_by:
                is_asc = sort_direction == "asc"
                stats_df = stats_df.sort_values(sort_by,ascending=is_asc)
            self._df = stats_df
        else:
            filter = expanded_df["Actor"] == name
            self._df = expanded_df[filter]
        return self

    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))