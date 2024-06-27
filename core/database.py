# Importa o 'sessionmaker' da SQLAlchemy para criar sessões de banco de dados
from sqlalchemy.orm import sessionmaker
# Importa 'create_async_engine' da SQLAlchemy para criar um motor assíncrono de banco de dados
from sqlalchemy.ext.asyncio import create_async_engine
# Importa 'AsyncEngine' da SQLAlchemy que representa o motor assíncrono do banco de dados
from sqlalchemy.ext.asyncio import AsyncEngine
# Importa 'AsyncSession' da SQLAlchemy que representa uma sessão assíncrona do banco de dados
from sqlalchemy.ext.asyncio import AsyncSession

# Importa as configurações (por exemplo, URL do banco de dados) do módulo 'core.configs'
from core.configs import settings

# Cria um motor assíncrono do banco de dados usando a URL fornecida nas configurações
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Configura a fábrica de sessões usando 'sessionmaker', que criará sessões assíncronas
Session: AsyncSession = sessionmaker(
    autocommit=False,            # Desativa o autocommit, exigindo commits explícitos nas transações
    autoflush=False,             # Desativa o autoflush, evitando que as alterações sejam enviadas automaticamente ao banco de dados
    expire_on_commit=False,      # Evita que as instâncias expirem após o commit, mantendo-as utilizáveis sem nova consulta ao banco de dados
    class_=AsyncSession,         # Define a classe da sessão como 'AsyncSession', tornando-a assíncrona
    bind=engine                  # Associa a sessão ao motor criado anteriormente, que gerencia a conexão com o banco de dados
)
