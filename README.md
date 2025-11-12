# FastAPI Project

API REST para **gestionar posts, usuarios y votos**, construida con **FastAPI + SQLModel**, **JWT**, **PostgreSQL** y **Alembic**.  
Sirve como plantilla base para desarrollar APIs modernas, seguras y fácilmente extensibles.

---

## Quickstart

### Requisitos

- **Python 3.11+**
- **PostgreSQL** en ejecución (local o remoto)
- **git** instalado

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<tu_usuario>/<tu_repo>.git
cd <tu_repo>

# Crear entorno virtual
python -m venv venv
# En Windows: venv\Scripts\activate
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Variables de entorno

Crea un archivo **.env** en la raíz del proyecto:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Migraciones y arranque

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Accede a:

- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc

---

## Estructura del proyecto

```
app/
  main.py           # Inicializa FastAPI y registra routers
  routers/          # posts.py, users.py, auth.py, votes.py
  models.py         # SQLModel (Posts, Users, Votes)
  schemas.py        # Pydantic (requests/responses)
  database.py       # Conexión y sesión con PostgreSQL
  oauth2.py         # Creación y validación de JWT
  utils.py          # Hashing con Argon2
alembic/
  env.py
  versions/         # Migraciones versionadas
requirements.txt
```

---

## Stack y decisiones técnicas

- **FastAPI + SQLModel**: validación automática y ORM tipado.  
- **PostgreSQL + Alembic**: persistencia estable y migraciones controladas.  
- **OAuth2 + JWT**: autenticación segura con tokens.  
- **Argon2 (pwdlib)**: cifrado robusto de contraseñas.  
- **pydantic-settings**: carga de configuración desde `.env`.  
- **CORS**: habilitado para desarrollo local.

---

## Endpoints principales

| Método | Ruta           | Descripción             | Auth |
|:-----:|-----------------|-------------------------|:----:|
| **POST**   | `/users`       | Crear usuario           | ❌   |
| **POST**   | `/login`       | Obtener token JWT       | ❌   |
| **GET**    | `/posts`       | Listar posts públicos   | ❌   |
| **POST**   | `/posts`       | Crear post              | ✅   |
| **PUT**    | `/posts/{id}`  | Actualizar post         | ✅   |
| **DELETE** | `/posts/{id}`  | Eliminar post           | ✅   |
| **POST**   | `/votes`       | Votar o retirar voto    | ✅   |

**Cabecera de autenticación:**

```
Authorization: Bearer <access_token>
```

---

## Migraciones Alembic

```bash
alembic upgrade head      # aplica migraciones
alembic revision -m "msg" # crea nueva migración
alembic downgrade -1      # revierte la última
```

> En producción usa exclusivamente **Alembic**; evita `SQLModel.metadata.create_all()`.

---

## Próximos pasos

- Añadir **tests automáticos** con `pytest`.  
- Crear un **Dockerfile** para despliegue completo.  
- Generar **datos seed** para entornos de demo.  
- Extender la documentación técnica en `docs/GUIDE.md`.

---

## Troubleshooting

| Problema | Causa probable | Solución |
|---------|-----------------|----------|
| No conecta a DB | `DATABASE_URL` incorrecta o Postgres no iniciado | Verificar credenciales y servicio |
| 401 Unauthorized | Falta token o token expirado | Regenerar JWT desde `/login` |
| CORS bloquea peticiones | Origen distinto al permitido | Añadir origen al middleware de CORS |

---

## Licencia

**MIT © 2025 [Beatriz]**
