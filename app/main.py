import pandas as pd
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .constants import DATA_PATH
from .routers import sales, pokemon, imdb1000

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup events
    app.state.sales_df = pd.read_csv(DATA_PATH / "Sales.csv", parse_dates=True, index_col=0).dropna(how="all").sort_index()

    pkmn_move_df = pd.read_csv(DATA_PATH / "move-data.csv", index_col=0).dropna(how="all").sort_index()
    pkmn_move_df['Type'] = pkmn_move_df['Type'].astype("category")
    pkmn_move_df['Category'] = pkmn_move_df['Category'].astype("category")
    pkmn_move_df['Contest'] = pkmn_move_df['Contest'].astype("category")
    app.state.pkmn_move_df = pkmn_move_df

    drop_cols = ["Poster_Link","Certificate"]
    imdb1000_df = pd.read_csv(DATA_PATH / "imdb-top-1000.csv").drop(columns=drop_cols).dropna(how="all").sort_index()
    imdb1000_df['Director'] = imdb1000_df['Director'].astype("category")
    imdb1000_df['Gross'] = imdb1000_df['Gross'].str.replace(",","").fillna(0).astype(int,errors='raise')
    app.state.imdb1000_df = imdb1000_df

    yield
    #shutdown events
    del app.state.df

app = FastAPI(lifespan=lifespan)
app.include_router(sales.router)
app.include_router(pokemon.router)
app.include_router(imdb1000.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my world!"}