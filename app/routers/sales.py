from fastapi import FastAPI, Query, APIRouter, Request

from ..data_processing import DataExplorer

app = FastAPI()
router = APIRouter(prefix="/api/sales")

@router.get("/summary")
async def read_summary_data(request: Request):
    data = DataExplorer(request.app.state.df)
    return data.summary().json_response()

@router.get("/kpis")
async def read_kpis(request: Request,country: str = Query(None)):
    data = DataExplorer(request.app.state.df)
    return data.kpis(country)

@router.get("")
async def read_sales(request: Request,limit: int = Query(100, gt=0, lt=150000)):
    data = DataExplorer(request.app.state.df,limit)
    return data.json_response()