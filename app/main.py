import pandas as pd
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .constants import DATA_PATH
from .routers import sales, pokemon

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup events
    app.state.sales_df = pd.read_csv(DATA_PATH / "Sales.csv", parse_dates=True, index_col=0).dropna(how="all").sort_index()

    pkmn_move_df = pd.read_csv(DATA_PATH / "move-data.csv", index_col=0).dropna(how="all").sort_index()
    pkmn_move_df['Type'] = pkmn_move_df['Type'].astype("category")
    pkmn_move_df['Category'] = pkmn_move_df['Category'].astype("category")
    pkmn_move_df['Contest'] = pkmn_move_df['Contest'].astype("category")
    app.state.pkmn_move_df = pkmn_move_df

    yield
    #shutdown events
    del app.state.df

app = FastAPI(lifespan=lifespan)
app.include_router(sales.router)
app.include_router(pokemon.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my world!"}