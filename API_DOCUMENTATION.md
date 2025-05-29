# Documentação da API SARA

## Índice
- [Autenticação](#autenticação)
- [Usuários](#usuários)
- [Tenants](#tenants)
- [Licenças](#licenças)

## Autenticação

### Login
```http
POST /api/v1/auth/login
```

**Descrição:** Realiza o login do usuário no sistema.

**Request Body:**
```json
{
    "email": "string",
    "password": "string",
    "remember_me": "boolean"
}
```

**Response (200):**
```json
{
    "access_token": "string",
    "user_id": "integer",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "is_verified": "boolean",
    "is_active": "boolean",
    "is_staff": "boolean",
    "is_superuser": "boolean"
}
```

## Usuários

### Criar Usuário
```http
POST /api/v1/users/
```

**Permissões:** SUPER_ADMIN, ADMIN

**Request Body:**
```json
{
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "password": "string",
    "tenant_id": "integer | null"
}
```

**Response (201):**
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "tenant_id": "integer | null",
    "is_verified": "boolean"
}
```

### Obter Usuário
```http
GET /api/v1/users/{user_id}
```

**Permissões:** ADMIN, USER

**Response (200):**
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "tenant_id": "integer | null",
    "is_verified": "boolean",
    "is_active": "boolean",
    "is_staff": "boolean",
    "is_superuser": "boolean"
}
```

### Ativar Usuário
```http
PUT /api/v1/users/{user_id}/activate
```

**Response (200):**
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "tenant_id": "integer | null",
    "is_verified": "boolean",
    "is_active": "boolean",
    "is_staff": "boolean",
    "is_superuser": "boolean"
}
```

## Tenants

### Criar Tenant
```http
POST /api/v1/tenants/tenants
```

**Request Body:**
```json
{
    "schema_name": "string",
    "name": "string",
    "domain": "string"
}
```

**Response (201):**
```json
{
    "id": "integer",
    "schema_name": "string",
    "name": "string",
    "domain": "string"
}
```

### Listar Tenants
```http
GET /api/v1/tenants/tenants
```

**Response (200):**
```json
[
    {
        "id": "integer",
        "schema_name": "string",
        "name": "string",
        "domain": "string"
    }
]
```

### Obter Tenant
```http
GET /api/v1/tenants/tenants/{schema_name}
```

**Response (200):**
```json
{
    "id": "integer",
    "schema_name": "string",
    "name": "string",
    "domain": "string"
}
```

## Licenças

### Criar Licença
```http
POST /api/v1/licenses/licenses
```

**Request Body:**
```json
{
    "tenant_id": "integer",
    "is_active": "boolean"
}
```

**Response (201):**
```json
{
    "id": "integer",
    "key": "uuid",
    "is_active": "boolean",
    "tenant_id": "integer"
}
```

### Listar Licenças
```http
GET /api/v1/licenses/licenses
```

**Response (200):**
```json
[
    {
        "id": "integer",
        "key": "uuid",
        "is_active": "boolean",
        "tenant_id": "integer"
    }
]
```

## Códigos de Erro

| Código | Tipo | Descrição |
|--------|------|-----------|
| 400 | VALIDATION_ERROR | Erro de validação nos dados enviados |
| 401 | INVALID_TOKEN | Token inválido ou expirado |
| 401 | INVALID_CREDENTIALS | Credenciais inválidas |
| 401 | EMAIL_NOT_FOUND | E-mail não encontrado |
| 403 | UNAUTHORIZED_ERROR | Acesso não autorizado |
| 404 | NOT_FOUND_ERROR | Recurso não encontrado |
| 500 | INTERNAL_SERVER_ERROR | Erro interno do servidor |

## Autenticação

A API usa autenticação JWT (JSON Web Token). Para acessar endpoints protegidos, inclua o token no header da requisição:

```http
Authorization: Bearer {seu_token_aqui}
```

## Multitenancy

O sistema utiliza uma arquitetura multitenancy, onde cada tenant possui seu próprio schema no banco de dados. O tenant é identificado pelo domínio da requisição ou pelo schema_name. 