import json
import pandas as pd
from fastapi.responses import JSONResponse

def get_generation_stats(df: pd.DataFrame):    
    stats_df = df.groupby("Generation").agg(
        Count=pd.NamedAgg(column="Name",aggfunc="count"),
        Avg_HP=pd.NamedAgg(column="HP", aggfunc="mean"),
        Max_HP=pd.NamedAgg(column="HP", aggfunc="max"),
        Min_HP=pd.NamedAgg(column="HP", aggfunc="min"),
        Avg_Attack=pd.NamedAgg(column="Attack", aggfunc="mean"),
        Max_Attack=pd.NamedAgg(column="Attack", aggfunc="max"),
        Min_Attack=pd.NamedAgg(column="Attack", aggfunc="min"),
        Avg_Defense=pd.NamedAgg(column="Defense", aggfunc="mean"),
        Max_Defense=pd.NamedAgg(column="Defense", aggfunc="max"),
        Min_Defense=pd.NamedAgg(column="Defense", aggfunc="min"),
        Avg_SpAtk=pd.NamedAgg(column="SpAtk", aggfunc="mean"),
        Max_SpAtk=pd.NamedAgg(column="SpAtk", aggfunc="max"),
        Min_SpAtk=pd.NamedAgg(column="SpAtk", aggfunc="min"),
        Avg_SpDef=pd.NamedAgg(column="SpDef", aggfunc="mean"),
        Max_SpDef=pd.NamedAgg(column="SpDef", aggfunc="max"),
        Min_SpDef=pd.NamedAgg(column="SpDef", aggfunc="min"),
        Avg_Speed=pd.NamedAgg(column="Speed", aggfunc="mean"),
        Max_Speed=pd.NamedAgg(column="Speed", aggfunc="max"),
        Min_Speed=pd.NamedAgg(column="Speed", aggfunc="min"),
    )
    return stats_df

class PokemonService:
    def __init__(self, df: pd.DataFrame, limit = 100):
        self._df_full = df
        self._df = df.head(limit)

    @property
    def df(self):
        return self.df
    
    def data(self,name,type,generation):
        if name:
            filter = self._df_full["Name"] == name
            self._df = self._df_full[filter]
            return self
        else:
            filtered_df = self._df_full
            if type:
                filter_type1 = filtered_df["Type1"] == type
                filter_type2 = filtered_df["Type2"] == type
                filtered_df = filtered_df[filter_type1 | filter_type2]
            if generation:
                filter_gen = filtered_df["Generation"] == generation
                filtered_df = filtered_df[filter_gen]
            self._df = filtered_df
            return self
    
    def generation(self,generation):
        if not generation:
            stats_df = get_generation_stats(self._df_full)
            self._df = stats_df
        else:
            filter = self._df_full["Generation"] == generation
            self._df = self._df_full[filter]
        return self

    def json_response(self):
        json_data = self._df.to_json(orient="records")
        return JSONResponse(json.loads(json_data))

class PokemonMoveService(PokemonService):
    def moves(self):
        return self

    def type(self, filter):
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