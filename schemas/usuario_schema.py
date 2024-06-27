# Importa Optional e List do módulo typing para especificar tipos opcionais e listas
from typing import Optional, List

# Importa BaseModel como SCBaseModel do Pydantic para definir esquemas de dados
from pydantic import BaseModel as SCBaseModel, EmailStr

# Importa ArtigoSchema do módulo schemas.artigo_schema para o esquema de dados do artigo
from schemas.artigo_schema import ArtigoSchema

# Define o esquema base para dados de usuário (não é um modelo ORM)
class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int] = None  # ID do usuário (opcional porque pode não estar presente em algumas operações)
    nome: str  # Nome do usuário (obrigatório)
    sobrenome: str  # Sobrenome do usuário (obrigatório)
    email: EmailStr  # Email do usuário, validado como EmailStr do Pydantic (obrigatório e válido)
    eh_admin: bool = False  # Indica se o usuário é administrador, padrão False se não especificado

    class Config:
        from_attributes = True  # Habilita o modo ORM para converter automaticamente de objetos SQLAlchemy

# Define o esquema para criação de um novo usuário, baseado no esquema base
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str  # Senha do usuário para criação (obrigatória)

# Define o esquema para dados de usuário que inclui artigos associados
class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]  # Lista opcional de artigos associados ao usuário, utilizando ArtigoSchema

# Define o esquema para atualização de dados de usuário, baseado no esquema base
class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str] = None # Nome do usuário (opcional para atualização)
    sobrenome: Optional[str] = None # Sobrenome do usuário (opcional para atualização)
    email: Optional[EmailStr] = None # Email do usuário (opcional para atualização)
    senha: Optional[str] = None # Senha do usuário (opcional para atualização)
    eh_admin: Optional[bool] = None # Indicação de administrador (opcional para atualização)
