import pandas as pd
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .constants import DATA_PATH
from .routers import sales

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup events
    app.state.df = pd.read_csv(DATA_PATH / "Sales.csv", parse_dates=True, index_col=0).sort_index()
    yield
    #shutdown events
    del app.state.df

app = FastAPI(lifespan=lifespan)
app.include_router(sales.router)