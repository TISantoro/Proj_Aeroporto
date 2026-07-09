# Sistema de Controle de Pousos e Decolagens

API REST desenvolvida com FastAPI para gerenciamento de pousos e decolagens em um aeroporto, com foco em aprendizado, mentoria e boas práticas no desenvolvimento de APIs.

Este projeto é uma base para estudo de:
- arquitetura em camadas
- autenticação com JWT
- hash de senhas com bcrypt
- testes automatizados
- organização de rotas, serviços, schemas e repositórios

## Tecnologias

- Python 3.13+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT (PyJWT)
- bcrypt
- Pytest

## Funcionalidades implementadas

- CRUD de usuários
- Login com JWT
- Hash de senha com bcrypt
- Proteção de rotas autenticadas
- Cadastro do primeiro usuário sem autenticação
- Testes automatizados para o fluxo de usuários

## Funcionalidades em desenvolvimento

- CRUD de aeronaves
- CRUD de pistas
- Operações de pouso e decolagem
- Auditoria
- Relatórios

## Pré-requisitos

- Python 3.10 ou superior
- pip
- virtualenv (opcional, mas recomendado)

## Instalação

Clone o repositório:

```bash
git clone https://github.com/TISantoro/Proj_Aeroporto.git
cd Proj_Aeroporto
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Inicie a aplicação:

```bash
python run.py
```

Ou com uvicorn:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

A documentação Swagger ficará disponível em:

- http://127.0.0.1:8000/docs

## Como usar a API

### 1. Criar o primeiro usuário

Endpoint:

```http
POST /users/
```

Body:

```json
{
  "name": "Admin",
  "email": "admin@email.com",
  "login": "admin",
  "password": "123456"
}
```

### 2. Fazer login

Endpoint:

```http
POST /auth/login
```

Body:

```json
{
  "login": "admin",
  "password": "123456"
}
```

Resposta:

```json
{
  "access_token": "<token_jwt>",
  "token_type": "bearer"
}
```

### 3. Usar o token nas rotas protegidas

No header da requisição:

```http
Authorization: Bearer <token_jwt>
```

## Estrutura do projeto

```text
app/
├── auth/               # JWT, hash de senha e dependências de autenticação
├── database/           # configuração do banco e sessão
├── models/             # modelos SQLAlchemy
├── repositories/       # acesso ao banco
├── routers/            # endpoints da API
├── schemas/            # modelos de entrada/saída com Pydantic
├── services/           # regras de negócio
```

## Testes

Execute os testes com:

```bash
pytest -q
```

## Fluxo de autenticação

- O primeiro usuário pode ser criado sem token. Isso permite inicializar o sistema quando ainda não existe nenhum usuário cadastrado
- Após existir pelo menos um usuário cadastrado, as rotas de criação e demais operações protegidas exigem autenticação via JWT.
