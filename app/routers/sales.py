from fastapi import FastAPI, Query, APIRouter, Request

from ..services.sales import SalesService

app = FastAPI()
router = APIRouter(prefix="/api/sales")

@router.get("/summary")
async def read_summary_data(request: Request):
    df = request.app.state.sales_df
    data = SalesService(df)
    return data.summary().json_response()

@router.get("/kpis")
async def read_kpis(request: Request,country: str = Query(None)):
    df = request.app.state.sales_df
    data = SalesService(df)
    return data.kpis(country)

@router.get("")
async def read_sales(request: Request,limit: int = Query(100, gt=0, lt=150000)):
    df = request.app.state.sales_df
    data = SalesService(df,limit)
    return data.json_response()