# Importa Column, Integer, String, ForeignKey do SQLAlchemy para definição de colunas e chaves estrangeiras
from sqlalchemy import Column, Integer, String, ForeignKey
# Importa relationship do SQLAlchemy para definir relacionamentos entre modelos
from sqlalchemy.orm import relationship

# Importa as configurações do banco de dados do módulo core.configs
from core.configs import settings

# Define a classe ArtigoModel, que herda de settings.DBBaseModel
class ArtigoModel(settings.DBBaseModel):
    __tablename__ = 'artigos'  # Nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Coluna ID como chave primária autoincrementável
    titulo = Column(String(256))  # Coluna para o título do artigo, tipo String com até 256 caracteres
    url_fonte = Column(String(256))  # Coluna para a URL da fonte do artigo, tipo String com até 256 caracteres
    descricao = Column(String(256))
    
    # Coluna para o ID do usuário que criou o artigo, chave estrangeira referenciando a tabela 'usuarios' e coluna 'id'
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    
    # Define o relacionamento com o modelo UsuarioModel
    criador = relationship(
        "UsuarioModel",  # Nome da classe do modelo relacionado
        back_populates='artigos',  # Nome do atributo no modelo UsuarioModel que faz referência a este relacionamento
        lazy='joined'  # Define o carregamento antecipado (eager loading) dos dados relacionados
    )
