import json
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse

def get_generation_stats(df: pd.DataFrame):
    df["Base_HP"] = np.where(df['isBase'], df['HP'], np.nan)
    df["Base_Attack"] = np.where(df['isBase'], df['Attack'], np.nan)
    df["Base_Defense"] = np.where(df['isBase'], df['Defense'], np.nan)
    df["Base_SpAtk"] = np.where(df['isBase'], df['SpAtk'], np.nan)
    df["Base_SpDef"] = np.where(df['isBase'], df['SpDef'], np.nan)
    df["Base_Speed"] = np.where(df['isBase'], df['Speed'], np.nan)

    stats_df = df.groupby("Generation").agg(
        Count=pd.NamedAgg(column="isBase",aggfunc="sum"),
        Mega_Count=pd.NamedAgg(column="isMega",aggfunc="sum"),
        Alternate_Form_Count=pd.NamedAgg(column="isAlternate",aggfunc="sum"),
        Total_Count=pd.NamedAgg(column="Name",aggfunc="count"),
        Avg_HP=pd.NamedAgg(column="Base_HP", aggfunc="mean"),
        Max_HP=pd.NamedAgg(column="Base_HP", aggfunc="max"),
        Min_HP=pd.NamedAgg(column="Base_HP", aggfunc="min"),
        Avg_Attack=pd.NamedAgg(column="Base_Attack", aggfunc="mean"),
        Max_Attack=pd.NamedAgg(column="Base_Attack", aggfunc="max"),
        Min_Attack=pd.NamedAgg(column="Base_Attack", aggfunc="min"),
        Avg_Defense=pd.NamedAgg(column="Base_Defense", aggfunc="mean"),
        Max_Defense=pd.NamedAgg(column="Base_Defense", aggfunc="max"),
        Min_Defense=pd.NamedAgg(column="Base_Defense", aggfunc="min"),
        Avg_SpAtk=pd.NamedAgg(column="Base_SpAtk", aggfunc="mean"),
        Max_SpAtk=pd.NamedAgg(column="Base_SpAtk", aggfunc="max"),
        Min_SpAtk=pd.NamedAgg(column="Base_SpAtk", aggfunc="min"),
        Avg_SpDef=pd.NamedAgg(column="Base_SpDef", aggfunc="mean"),
        Max_SpDef=pd.NamedAgg(column="Base_SpDef", aggfunc="max"),
        Min_SpDef=pd.NamedAgg(column="Base_SpDef", aggfunc="min"),
        Avg_Speed=pd.NamedAgg(column="Base_Speed", aggfunc="mean"),
        Max_Speed=pd.NamedAgg(column="Base_Speed", aggfunc="max"),
        Min_Speed=pd.NamedAgg(column="Base_Speed", aggfunc="min"),
    )

    df = stats_df.drop(stats_df.filter(like='Base_').columns, axis=1)

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
    
    def generation(self,generation,show_variant):
        if not generation:
            stats_df = get_generation_stats(self._df_full)
            self._df = stats_df
        else:
            filter1 = self._df_full["Generation"] == generation
            if show_variant:
                filter2 = self._df_full["isBase"] | self._df_full["isVariant"]
            else:
                filter2 = self._df_full["isBase"]
            self._df = self._df_full[filter1 & filter2]
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