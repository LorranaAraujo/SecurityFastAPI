from pymongo import MongoClient
from ..models.viewmodels import Tarefa
from bson import ObjectId
from typing import Union, Optional, Dict, List
from decouple import config

class MongoDbRepository:
    def __init__(self):
        #uri = 'mongodb://localhost:27017'
        uri = config('uri_mongo')
        client = MongoClient(uri)
        db = client['tasksWeb']
        self.tarefas = db['tasks']

    def criarTarefa(self, tarefa) -> str:
        _id = self.tarefas.insert_one(tarefa.toDict()).inserted_id
        tarefa.id = str(_id)
        return {'mensagem': 'Tarefa criada'}
    
    def mostrarTarefas(self) -> List:
        tarefas = self.tarefas.find()
        return list(map(Tarefa.fromDict, tarefas))
    
    def mostrarById(self, id) -> Optional[Union[Tarefa, Dict[str, str]]]:
        if len(id) != 24:
            return {'mensagem': 'erro na quantidade de caracteres'}
        filtro = {"_id": ObjectId(id)}
        tarefa_encontrada = self.tarefas.find_one(filtro)
        if tarefa_encontrada:
            return Tarefa.fromDict(tarefa_encontrada)
        return {"mensagem","tarefa nao encontrada"}
    
    def deletarTarefa(self, id) -> None:
        if len(id) != 24:
            return {'mensagem': 'erro na quantidade de caracteres'}
        filtro = {'_id': ObjectId(id)}
        tarefa_encontrada = self.tarefas.find_one(filtro)
        if tarefa_encontrada:
            self.tarefas.delete_one(tarefa_encontrada)
            return {'mensagem': 'tarefa deletada'}
        return {'mensagem': 'tarefa nao encontrada'}
    
    def atualizarTarefa(self, id, tarefa) -> Optional[Tarefa]:
        filtro = {"_id": ObjectId(id)}
        self.tarefas.update_one(filtro, {'$set': tarefa.toDict()})
        tarefa.id = id
        return tarefa
