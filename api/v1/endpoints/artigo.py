# Importa List do módulo typing para especificar listas
from typing import List

# Importa dependências do FastAPI, incluindo APIRouter, status, Depends, HTTPException, Response
from fastapi import APIRouter, status, Depends, HTTPException, Response

# Importa AsyncSession e select do SQLAlchemy para operações assíncronas com o banco de dados
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Importa os modelos ArtigoModel e UsuarioModel
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel

# Importa o esquema ArtigoSchema
from schemas.artigo_schema import ArtigoSchema

# Importa dependências get_session e get_current_user
from core.deps import get_session, get_current_user

# Cria um roteador APIRouter para organizar as rotas
router = APIRouter()

# POST Artigo
@router.post("/", response_model=ArtigoSchema, status_code=status.HTTP_201_CREATED)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    # Cria uma nova instância de ArtigoModel com os dados fornecidos
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo, 
        descricao=artigo.descricao, 
        url_fonte=str(artigo.url_fonte), 
        usuario_id=usuario_logado.id
    )
    
    # Adiciona o novo artigo ao banco de dados
    db.add(novo_artigo)
    await db.commit()
    
    # Retorna o novo artigo criado
    return novo_artigo

# GET Artigos - Consultas são sempre seguras
@router.get("/", response_model=List[ArtigoSchema], status_code=status.HTTP_200_OK)
async def get_artigos(db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar todos os artigos
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        
        # Retorna a lista de artigos
        return artigos

# GET Artigo - Consultas são sempre seguras
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um artigo pelo ID
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        
        # Se o artigo for encontrado, retorna-o, caso contrário, lança uma exceção HTTP 404
        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# PUT Artigo
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um artigo pelo ID
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()
        
        # Se o artigo for encontrado, atualiza seus campos
        if artigo_up:
            if artigo.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_up.url_fonte = str(artigo.url_fonte)
            if usuario_logado.id != artigo_up.usuario_id:
                artigo_up.usuario_id = usuario_logado.id
            
            # Confirma as mudanças no banco de dados
            await session.commit()
            
            # Retorna o artigo atualizado
            return artigo_up
        else:
            # Se o artigo não for encontrado, lança uma exceção HTTP 404
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Artigo
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um artigo pelo ID e pelo ID do usuário logado
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()
        
        # Se o artigo for encontrado, exclui-o do banco de dados
        if artigo_del:
            await session.delete(artigo_del)
            await session.commit()
            
            # Retorna uma resposta HTTP 204 No Content
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            # Se o artigo não for encontrado, lança uma exceção HTTP 404
            raise HTTPException(detail='Artigo não encontrado', status_code=status.HTTP_404_NOT_FOUND)
