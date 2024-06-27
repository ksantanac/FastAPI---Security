# Importa Generator para especificar o tipo de retorno da função
from typing import Generator, Optional

# Importa Depends e HTTPException do FastAPI para gerenciar dependências e exceções HTTP
from fastapi import Depends, HTTPException, status
# Importa jwt e JWTError da biblioteca jose para manipulação de JWT e tratamento de erros
from jose import jwt, JWTError

# Importa AsyncSession para sessões assíncronas com SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
# Importa select para consultas com SQLAlchemy
from sqlalchemy.future import select
# Importa BaseModel do Pydantic para criar modelos de dados
from pydantic import BaseModel

# Importa o objeto Session, que é configurado para criar sessões de banco de dados
from core.database import Session
# Importa o esquema OAuth2 para autenticação
from core.auth import oauth2_schema
# Importa configurações do módulo core.configs
from core.configs import settings
# Importa o modelo de usuário do módulo models
from models.usuario_model import UsuarioModel

# Define um modelo Pydantic para dados de token
class TokenData(BaseModel):
    username: Optional[str] = None

# Define uma função assíncrona chamada get_session que retorna um Generator
async def get_session() -> Generator:
    # Cria uma nova sessão assíncrona do SQLAlchemy
    session: AsyncSession = Session()
    
    try:
        # O bloco try é usado para garantir que a sessão seja fechada corretamente
        yield session  # Yield retorna a sessão para ser usada no contexto atual (por exemplo, dentro de uma rota FastAPI)
    finally:
        # O bloco finally é sempre executado, garantindo que a sessão seja fechada mesmo se ocorrer uma exceção
        await session.close()  # Fecha a sessão assíncrona

# Define uma função assíncrona para obter o usuário atual
async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    
    # Define uma exceção de credenciais para ser usada em caso de falha na autenticação
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token JWT usando o segredo e o algoritmo especificados nas configurações
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            # Desativa a verificação do campo 'aud' (audience) no token
            options={"verify_aud": False},
        )
        
        # Obtém o campo "sub" (assunto) do payload, que deve conter o username
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Cria um objeto TokenData com o username decodificado do token
        token_data: TokenData = TokenData(username=username)
        
    except JWTError:
        # Lança uma exceção se houver um erro ao decodificar o token
        raise credentials_exception
    
    # Abre uma sessão assíncrona com o banco de dados
    async with db as session:
        # Cria uma consulta para selecionar o usuário pelo ID obtido do token
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))
        # Executa a consulta de forma assíncrona
        result = await session.execute(query)
        # Obtém o usuário da consulta
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
        if usuario is None:
            # Lança uma exceção se o usuário não for encontrado
            raise credentials_exception
        
        # Retorna o usuário autenticado
        return usuario
