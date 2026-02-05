import pandas as pd
from fastapi import FastAPI, Query, APIRouter
from contextlib import asynccontextmanager

from constants import DATA_PATH
from data_processing import DataExplorer

# allows csv to read it once only
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_csv(DATA_PATH / "Sales.csv", parse_dates=True, index_col=0).sort_index()
    yield
    del app.state.df

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/sales")

@router.get("/summary")
async def read_summary_data():
    data = DataExplorer(app.state.df)
    return data.summary().json_response()

@router.get("/kpis")
async def read_kpis(country: str = Query(None)):
    data = DataExplorer(app.state.df)
    return data.kpis(country)

@router.get("")
# 'limit' is a URL parameter
async def read_sales(limit: int = Query(100, gt=0, lt=150000)):
    data = DataExplorer(app.state.df,limit)
    return data.json_response()

app.include_router(router)