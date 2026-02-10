import json
import pandas as pd
from fastapi.responses import JSONResponse

def get_stats_by_column(df:pd.DataFrame, col_name:str) -> pd.DataFrame:
    count = df.groupby(col_name).agg({"Series_Title":"count"}).reset_index()
    count = count.rename(columns={"Series_Title":"Movie_Count"})

    gross_total = df.groupby(col_name).agg({"Gross":"sum"}).reset_index()
    gross_total = gross_total.drop(columns="Director").add_prefix("Total_")

    metrics_mean = df.groupby(col_name).agg({"Gross":"mean","IMDB_Rating":"mean","Meta_score":"mean"}).reset_index()
    metrics_mean = metrics_mean.drop(columns="Director").add_prefix("Avg_")

    stats_df = pd.concat([count,gross_total,metrics_mean], axis="columns")
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
            stats_df = get_stats_by_column(self._df_full, "Director")
            if sort_by:
                is_asc = sort_direction == "asc"
                stats_df = stats_df.sort_values(sort_by,ascending=is_asc)
            self._df = stats_df
        else:
            filter = self._df_full["Director"] == name
            self._df = self._df_full[filter]
        return self

    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))