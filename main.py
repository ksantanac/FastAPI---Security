from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title="Curso API - Segurança")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)


    """
    Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzIwMDQ4NDI1LCJpYXQiOjE3MTk0NDM2MjUsInN1YiI6IjIifQ.quQJ24oOYqV7ADuOPNxzKEf5KZQB1vAi4Apz42RfFug
    Tipo: bearer
    
    
    Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzIwMDUxMTg0LCJpYXQiOjE3MTk0NDYzODQsInN1YiI6IjMifQ.hJur2xTpnDk8ZDV0Fc9YBFR8H3J7qPatkltl492OIWE
    Tipo: bearer
    
    """