# Importa List, Optional e Any do módulo typing para especificar tipos
from typing import List, Optional, Any

# Importa dependências do FastAPI, incluindo APIRouter, status, Depends, HTTPException, Response, OAuth2PasswordRequestForm, e JSONResponse
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# Importa AsyncSession e select do SQLAlchemy para operações assíncronas com o banco de dados
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

# Importa os modelos UsuarioModel
from models.usuario_model import UsuarioModel

# Importa os esquemas de usuário
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaArtigos, UsuarioSchemaUp

# Importa dependências get_session e get_current_user
from core.deps import get_session, get_current_user

# Importa funções para hash de senha e autenticação
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

# Cria um roteador APIRouter para organizar as rotas
router = APIRouter()

# GET logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    # Retorna o usuário atualmente logado
    return usuario_logado

# POST / SignUP 
@router.post("/signup", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    # Cria uma nova instância de UsuarioModel com os dados fornecidos
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin
    )
    
    # Adiciona o novo usuário ao banco de dados e confirma a transação
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
        
            # Retorna o novo usuário criado
            return novo_usuario
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail="Já existe um usuário com esse e-mail já cadastrado."
                )

# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar todos os usuários
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        # Retorna a lista de usuários
        return usuarios

# GET Usuario
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um usuário pelo ID
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        # Se o usuário for encontrado, retorna-o, caso contrário, lança uma exceção HTTP 404
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuario não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# PUT Usuario
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um usuário pelo ID
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        
        # Se o usuário for encontrado, atualiza seus campos
        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
           
            # Confirma as mudanças no banco de dados
            await session.commit()

            # Retorna o usuário atualizado
            return usuario_up
        else:
            # Se o usuário não for encontrado, lança uma exceção HTTP 404
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    # Abre uma sessão assíncrona
    async with db as session:
        # Executa uma consulta para selecionar um usuário pelo ID
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        # Se o usuário for encontrado, exclui-o do banco de dados
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            # Retorna uma resposta HTTP 204 No Content
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            # Se o usuário não for encontrado, lança uma exceção HTTP 404
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

# POST Login
@router.post("/login")
async def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    # Autentica o usuário com base nos dados do formulário
    usuario = await autenticar(
        email=form_data.username,
        senha=form_data.password,
        db=db
    )
    
    # Se a autenticação falhar, lança uma exceção HTTP 400
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados de acesso incorretos."
            )
    
    # Retorna o token de acesso para o usuário autenticado
    return JSONResponse(
        content={"acess_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )
    
    # Se a autenticação for bem-sucedida, a função criar_token_acesso é chamada para gerar um token de acesso (access_token). O ID do usuário (usuario.id) é passado como o "subject" (sub) do token.
    # criar_token_acesso é uma função que gera um JWT (JSON Web Token) para autenticação.
    # Um JSONResponse é retornado com:
    # O conteúdo (content) contendo o token de acesso e o tipo de token (bearer).
    # O status HTTP 200 (OK), indicando que a autenticação foi bem-sucedida.
