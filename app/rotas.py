from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import APIRouter, Body, Request, HTTPException, status, FastAPI, requests
from .classes import AcelerometroModel
router = APIRouter(prefix='/acelerometro', tags=['acelerometro'])

@router.post('/acelerometro/{empresa}/{equip}/{ax}/{ay}/{az}/{temp}',response_model=AcelerometroModel)
async def salvar_dados_acelerometro(request: Request,empresa:str,equip:str,ax :float,ay:float,az:float,temp:float):
    dados_acelerometro = {"nome_empresa":empresa,
                         "nome_equip":equip,
                         "acelerometroX": ax,
                         "acelerometroY": ay,
                         "acelerometroZ": az,
                         "temp":temp,
                         "dt_cria": (datetime.now())
                          }
    acelerometro_json = jsonable_encoder(dados_acelerometro)
    db = request.app.state.mongodb.db_acelerometro
    acelerometro_nova= await db["acelerometro"].insert_one(acelerometro_json)   
    inserted_id = str(acelerometro_nova.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": inserted_id})

@router.post('/acelerometro',response_model=AcelerometroModel)
async def salvar_dados_acelerometro_json(request: Request, data: AcelerometroModel):
    dados_acelerometro = {
        'nome_empresa':data.nome_empresa,
        "nome_equip": data.nome_equip,
        "acelerometroX": data.acelerometroX,
        "acelerometroY": data.acelerometroY,
        "acelerometroZ": data.acelerometroZ,
        'temp':data.temp,
        "dt_cria": datetime.now()
    }
    acelerometro_json = jsonable_encoder(dados_acelerometro)
    db = request.app.state.mongodb.db_acelerometro
    acelerometro_nova= await db["acelerometro"].insert_one(acelerometro_json)   
    inserted_id = str(acelerometro_nova.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": inserted_id})

@router.get('/acelerometro/{qtd}/{empresa}')
async def recuperar_dados_acelerometro_json(request: Request, qtd: int): 
    db = request.app.state.mongodb.db_acelerometro
    dados = await db["acelerometro"].find().to_list(qtd)
    for item in dados:
        item['_id'] = str(item['_id'])
    return dados