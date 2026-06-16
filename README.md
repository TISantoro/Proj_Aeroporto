# Sistema de Controle de Pousos e Decolagens

## 📁 Estrutura do Projeto

```
Proj_Aeroporto/
├── app/
│   ├── __init__.py
│   ├── main.py                 # App FastAPI principal
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py              # Configuração do banco de dados
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Modelo de Usuário (ORM)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py            # Schemas de validação (Pydantic)
│   └── routers/
│       ├── __init__.py
│       └── users.py           # Endpoints da API de usuários
├── main.py                     # Ponto de entrada
├── run.py                      # Script para rodar o servidor
└── requirements.txt            # Dependências do projeto
```

## 🚀 Como Começar

### 1. Rodar o servidor
```bash
python run.py
```
O servidor vai rodar em: http://localhost:8000

### 3. Acessar a documentação interativa
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📝 US-01: Cadastrar Usuário

### O que foi implementado:

**Endpoint:** `POST /users/`

**Campos do cadastro:**
- `name` (string) - Nome do usuário
- `email` (string) - Email único
- `login` (string) - Login único
- `password` (string) - Senha

**Validações:**
- Email e login devem ser únicos
- Email deve ser válido
- Todos os campos são obrigatórios

**Exemplo de requisição (via Swagger UI ou curl):**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "login": "joao_silva",
    "password": "senha123"
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com",
  "login": "joao_silva",
  "active": true,
  "created_at": "2026-06-16T12:00:00",
  "updated_at": "2026-06-16T12:00:00"
}
```
