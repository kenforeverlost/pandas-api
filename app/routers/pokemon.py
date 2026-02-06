from fastapi import FastAPI, Query, APIRouter, Request

from ..services.pokemon import PokemonService

app = FastAPI()
router = APIRouter(prefix="/api/pokemon")

@router.get("/moves")
async def read_moves(request: Request):
    df = request.app.state.pkmn_move_df
    data = PokemonService(df)
    return data.moves().json_response()

@router.get("/moves/type")
async def read_moves_by_type(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonService(df)
    return data.type(filter).json_response()

@router.get("/moves/category")
async def read_moves_by_category(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonService(df)
    return data.category(filter).json_response()

@router.get("/moves/contest")
async def read_moves_by_contest(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonService(df)
    return data.contest(filter).json_response()