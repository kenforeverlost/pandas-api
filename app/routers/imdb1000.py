from fastapi import FastAPI, Query, APIRouter, Request

from ..services.imdb1000 import Imdb1000Service

app = FastAPI()
router = APIRouter(prefix="/api/imdb1000")

@router.get("")
async def read_movies(request: Request):
    df = request.app.state.imdb1000_df
    data = Imdb1000Service(df)
    return data.imdb1000().json_response()

@router.get("/director/{name}")
async def read_movies_by_director(
    request: Request,
    name: str,
    sort_by: str = Query(None),
    sort_direction: str = Query("asc"),
):
    df = request.app.state.imdb1000_df
    data = Imdb1000Service(df)
    return data.director(name,sort_by,sort_direction).json_response()

@router.get("/director")
async def read_movies_by_director(
    request: Request,
    sort_by: str = Query(None),
    sort_direction: str = Query("asc"),
):
    name=None
    df = request.app.state.imdb1000_df
    data = Imdb1000Service(df)
    return data.director(name,sort_by,sort_direction).json_response()

@router.get("/actor/{name}")
async def read_movies_by_actor(
    request: Request,
    name: str,
    sort_by: str = Query(None),
    sort_direction: str = Query("asc"),
):
    df = request.app.state.imdb1000_df
    data = Imdb1000Service(df)
    return data.actor(name,sort_by,sort_direction).json_response()

@router.get("/actor")
async def read_movies_by_actor(
    request: Request,
    sort_by: str = Query(None),
    sort_direction: str = Query("asc"),
):
    name=None
    df = request.app.state.imdb1000_df
    data = Imdb1000Service(df)
    return data.actor(name,sort_by,sort_direction).json_response()