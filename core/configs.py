
from typing import List, ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

# Definição da classe de configurações usando Pydantic
class Settings(BaseSettings):
    # Prefixo da versão da API
    API_V1_STR: str = '/api/v1'
    
    # URL de conexão com o banco de dados PostgreSQL usando asyncpg
    DB_URL: str = "postgresql+asyncpg://postgres:rekaue13@localhost:5432/faculdade"
    DBBaseModel: ClassVar  = declarative_base()
    
    JWT_SECRET: str = 'hQlNazexOSjAZpcEm9ZH6YrmOWRI9OJn47El7WdC0Gs'
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """
    
    
    ALGORITHM: str = 'HS256'
    
    # 60 minutos * 24h * 7 dias
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    
    # Classe interna para configurações adicionais
    class Config:
        # Sensibilidade a maiúsculas/minúsculas para variáveis de ambiente
        case_sensitive = True
        
# Instanciação do objeto de configurações
settings: Settings = Settings()
