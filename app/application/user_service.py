from fastapi import Depends, HTTPException, status

from ..infra.cryptograph.hash_provider import HashProvider
from ..repository.auth_mongoDB_repository import AuthMongoDBRepository


class UsuarioService():

    def __init__(self,auth_repository=Depends(AuthMongoDBRepository),hash_provider=Depends(HashProvider)):
        self.auth_repository = auth_repository
        self.hash_provider = hash_provider

    def criar_usuario(self, usuario):
        if usuario.senha != usuario.confirmacao_senha:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Senhas não conferem!')

        usuario_usuario = self.auth_repository.obter_usuario_por_usuario(usuario.usuario)

        if usuario_usuario:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário(login) já utilizado!')

        usuario_email = self.auth_repository.obter_usuario_por_email(usuario.email)
        if usuario_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Email já cadastrado!')

        usuario.senha = self.hash_provider.hash_senha(usuario.senha)
        usuario_criado = self.auth_repository.criar_usuario(usuario)
        return usuario_criado