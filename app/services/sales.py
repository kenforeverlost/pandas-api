import json
import pandas as pd
from fastapi.responses import JSONResponse

class SalesService:
    def __init__(self, df: pd.DataFrame, limit = 100):
        self._df_full = df
        self._df = df.head(limit)

    #access DataFrame
    @property
    def df(self):
        return self.df
    
    def summary(self):
        drop_columns = ["count"]
        drop_rows = ["Day","Year"]
        self._df = self._df_full.describe().drop(drop_columns).drop(drop_rows,axis=1).T.reset_index()
        return self
    
    def kpis(self, country):
        if not country:
            df = self._df_full
        else:
            df = self._df_full.query("Country.str.casefold() == @country")
        return {
            "total_revenue": str(df["Revenue"].sum()),
            "total_profit": str(df["Profit"].sum()),
            "total_cost": str(df["Cost"].sum()),
            "num_of_purchases": str(len(df))
        }
    
    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))