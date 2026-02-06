import json
import pandas as pd
from fastapi.responses import JSONResponse

class PokemonService:
    def __init__(self, df: pd.DataFrame, limit = 100):
        self._df_full = df
        self._df = df.head(limit)

    #access DataFrame
    @property
    def df(self):
        return self.df
    
    def moves(self):
        return self
    
    def type(self, filter, show_stats):
        if not filter:
            self._df = self._df_full['Type'].value_counts().to_frame().reset_index()
        else:
            filter = self._df_full["Type"] == filter
            self._df = self._df_full[filter]
        return self
    
    def category(self, filter):
        if not filter:
            self._df = self._df_full['Category'].value_counts().to_frame().reset_index()
        else:
            filter = self._df_full["Category"] == filter
            self._df = self._df_full[filter]
        return self
    
    def contest(self, filter):
        if not filter:
            self._df = self._df_full['Contest'].value_counts().to_frame().reset_index()
        else:
            filter = self._df_full["Contest"] == filter
            self._df = self._df_full[filter]
        return self

    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))