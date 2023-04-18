from fastapi import APIRouter, status
from ..viewmodels import Tarefa
from ...repository.mongoDB_repository import MongoDbRepository


routes = APIRouter()
prefix = '/tarefas'

@routes.post('/', status_code=status.HTTP_201_CREATED)
async def criar_tarefa(tarefa: Tarefa):
    return MongoDbRepository().criarTarefa(tarefa)

@routes.get('/', status_code=status.HTTP_200_OK)
async def mostrar_tarefas():
    return MongoDbRepository().mostrarTarefas()

@routes.get('/{id}', status_code=status.HTTP_200_OK)
async def mostrar_by_id(id: str):
    return MongoDbRepository().mostrarById(id)

@routes.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(id: str):
    return MongoDbRepository().deletarTarefa(id)

@routes.put('/{id}')
async def atualizar_tarefa(id: str, tarefa: Tarefa):
    return MongoDbRepository().atualizarTarefa(id, tarefa)