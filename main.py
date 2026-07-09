from fastapi import FastAPI
from app.auth import router as auth_router
from app.database.db import engine, Base
from app.routers import users

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Controle de Pousos e Decolagens",
    description="API para gerenciar aeroporto",
    version="1.0.0"
)

# Inclui os routers
app.include_router(auth_router.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo ao Sistema de Controle de Pousos e Decolagens",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

