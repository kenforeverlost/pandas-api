from fastapi import FastAPI, Query, APIRouter, Request

from ..services.pokemon import PokemonService, PokemonMoveService

app = FastAPI()
router = APIRouter(prefix="/api/pokemon")

@router.get("/")
async def read_pokemon(
    request: Request,
    type: str = Query(None),
    generation: int = Query(None)
):
    df = request.app.state.pkmn_df
    data = PokemonService(df)
    return data.data(None,type,generation).json_response()

@router.get("/moves")
async def read_moves(request: Request):
    df = request.app.state.pkmn_move_df
    data = PokemonMoveService(df)
    return data.moves().json_response()

@router.get("/moves/type")
async def read_moves_by_type(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonMoveService(df)
    return data.type(filter).json_response()

@router.get("/moves/category")
async def read_moves_by_category(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonMoveService(df)
    return data.category(filter).json_response()

@router.get("/moves/contest")
async def read_moves_by_contest(request: Request,filter: str = Query(None)):
    df = request.app.state.pkmn_move_df
    data = PokemonMoveService(df)
    return data.contest(filter).json_response()

@router.get("/generation")
async def read_pokemon_by_generation(
    request: Request,
    generation: int = Query(None)
):
    df = request.app.state.pkmn_df
    data = PokemonService(df)
    return data.generation(generation).json_response()

@router.get("/{name}")
async def read_pokemon(request: Request,name: str):
    df = request.app.state.pkmn_df
    data = PokemonService(df)
    return data.data(name,None,None).json_response()