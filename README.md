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

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar o servidor
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

---

## 🎯 Próximas Melhorias para Aprender

### 1. **Hashear a senha** ⚠️ IMPORTANTE
- [ ] Instalar `bcrypt` ou `passlib`
- [ ] Implementar hash de senha antes de salvar
- [ ] Criar função de validação de senha

### 2. **Validações mais robustas**
- [ ] Validar comprimento mínimo de senha
- [ ] Validar formato de email mais rigoroso
- [ ] Adicionar validação de CPF (se necessário)

### 3. **Testes automatizados**
- [ ] Criar testes unitários com `pytest`
- [ ] Testar casos de sucesso e erro

### 4. **Autenticação**
- [ ] Implementar JWT para login
- [ ] Criar endpoint de login

---

## 📚 Conceitos para Entender

### 1. **Models (SQLAlchemy)**
- Classe que representa a tabela no banco de dados
- Define a estrutura dos dados (colunas, tipos, relacionamentos)

### 2. **Schemas (Pydantic)**
- Valida e serializa dados da API
- Transforma dados Python em JSON

### 3. **Routers (FastAPI)**
- Agrupa endpoints relacionados
- Define o comportamento dos endpoints

### 4. **Database Session**
- `get_db()` injeta a sessão do banco automaticamente
- Garante que a conexão seja fechada

---

## 💡 Dicas de Desenvolvimento

1. **Use o Swagger UI** para testar a API enquanto desenvolve
2. **Leia os erros** - FastAPI dá mensagens muito claras
3. **Incremente gradualmente** - faça uma coisa por vez
4. **Commite frequentemente** - bom para histórico

---

## 🔗 Recursos Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

**Pronto para começar? Rode `python run.py` e acesse http://localhost:8000/docs!** 🎉
