from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..infra.cryptograph.token_provider import JWTTokenProvider
from ..repository.auth_mongoDB_repository import AuthMongoDBRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl='signin')


async def obter_usuario_logado(
        token: str = Depends(oauth2_schema),
        jwt_provider=Depends(JWTTokenProvider),
        auth_repository=Depends(AuthMongoDBRepository)):
    
    try:
        payload = jwt_provider.decode(token)
        usuario_id = payload['usuario_id']
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido!')

    usuario = auth_repository.obter_usuario_por_id(usuario_id)

    return usuario