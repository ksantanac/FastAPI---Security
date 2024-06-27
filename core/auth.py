# Importa timezone da biblioteca pytz para trabalhar com fusos horários
from pytz import timezone

# Importa tipos opcionais e listas do módulo typing
from typing import Optional, List
# Importa datetime e timedelta da biblioteca datetime para manipulação de datas e tempos
from datetime import datetime, timedelta

# Importa OAuth2PasswordBearer do FastAPI para autenticação com OAuth2
from fastapi.security import OAuth2PasswordBearer

# Importa select da futura versão do SQLAlchemy para consultas
from sqlalchemy.future import select
# Importa AsyncSession da SQLAlchemy para sessões assíncronas
from sqlalchemy.ext.asyncio import AsyncSession

# Importa jwt da biblioteca jose para trabalhar com JSON Web Tokens (JWT)
from jose import jwt

# Importa o modelo de usuário do módulo models
from models.usuario_model import UsuarioModel
# Importa configurações do módulo core.configs
from core.configs import settings
# Importa função para verificar senha do módulo core.security
from core.security import verificar_senha

# Importa EmailStr do Pydantic para validação de email
from pydantic import EmailStr

# Define o esquema OAuth2 para autenticação, especificando a URL de login
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

# Função assíncrona para autenticar um usuário
async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:  # Abre uma sessão assíncrona
        # Cria uma consulta para selecionar o usuário pelo email
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        # Executa a consulta de forma assíncrona
        result = await session.execute(query)
        # Obtém o usuário da consulta
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
        if not usuario:  # Se o usuário não foi encontrado, retorna None
            return None
        
        # Verifica se a senha está correta
        if not verificar_senha(senha, usuario.senha):
            return None
        
        return usuario  # Retorna o usuário se a autenticação foi bem-sucedida

# Função privada para criar um token
def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # Define o payload do token de acordo com a especificação JWT (RFC 7519)
    payload = {}
    
    # Define o fuso horário para São Paulo
    sp = timezone('America/Sao_Paulo')
    # Calcula a data de expiração do token
    expira = datetime.now(tz=sp) + tempo_vida
    
    payload["type"] = tipo_token  # Define o tipo de token no payload
    payload["exp"] = expira  # Define a data de expiração no payload
    payload["iat"] = datetime.now(tz=sp)  # Define a data de criação no payload
    payload["sub"] = str(sub)  # Define o assunto (sub) no payload
    
    # Codifica o payload em um token JWT usando o segredo e o algoritmo especificados
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

# Função para criar um token de acesso
def criar_token_acesso(sub: str) -> str:
    """
    http://jwt.io
    """
    # Chama a função privada _criar_token para criar o token de acesso
    return _criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
