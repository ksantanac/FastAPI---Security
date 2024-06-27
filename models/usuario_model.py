# Importa Integer, String, Column, Boolean do SQLAlchemy para definição de colunas
from sqlalchemy import Integer, String, Column, Boolean
# Importa relationship do SQLAlchemy para definir relacionamentos entre modelos
from sqlalchemy.orm import relationship

# Importa as configurações do banco de dados do módulo core.configs
from core.configs import settings

# Define a classe UsuarioModel, que herda de settings.DBBaseModel
class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'  # Nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Coluna ID como chave primária autoincrementável
    nome = Column(String(256), nullable=True)  # Coluna para o nome do usuário, tipo String com até 256 caracteres, permite valores nulos
    sobrenome = Column(String(256), nullable=True)  # Coluna para o sobrenome do usuário, tipo String com até 256 caracteres, permite valores nulos
    email = Column(String(256), index=True, nullable=False, unique=True)  # Coluna para o email do usuário, tipo String com até 256 caracteres, indexada, não permite valores nulos, único
    senha = Column(String(256), nullable=False)  # Coluna para a senha do usuário, tipo String com até 256 caracteres, não permite valores nulos
    eh_admin = Column(Boolean, default=False)  # Coluna para indicar se o usuário é administrador, tipo Boolean, padrão False
    
    # Define o relacionamento com o modelo ArtigoModel
    artigos = relationship(
        "ArtigoModel",  # Nome da classe do modelo relacionado
        cascade="all, delete-orphan",  # Define a ação de cascata para todas as operações e exclusão de órfãos
        back_populates="criador",  # Nome do atributo no modelo ArtigoModel que faz referência a este relacionamento
        uselist=True,  # Define se a relação é para uma lista de objetos (True) ou um único objeto (False)
        lazy="joined"  # Define o carregamento antecipado (eager loading) dos dados relacionados
    )
