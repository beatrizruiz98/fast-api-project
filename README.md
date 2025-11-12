# 🧩 FastAPI Project

API REST para **gestionar posts, usuarios y votos**, construida con **FastAPI + SQLModel**, **JWT**, **PostgreSQL** y **Alembic**.  
Pensada como plantilla educativa o punto de partida para proyectos reales.

---

## 🚀 Quickstart

### 1️⃣ Requisitos
- Python 3.11+
- PostgreSQL activo (local o remoto)
- `git` instalado

### 2️⃣ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<tu_usuario>/<tu_repo>.git
cd <tu_repo>

# Crear entorno virtual
python -m venv venv
source venv/bin/activate     # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
3️⃣ Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto (no se sube a GitHub):

env
Copy code
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
4️⃣ Ejecutar migraciones y levantar el servidor
bash
Copy code
alembic upgrade head
uvicorn app.main:app --reload
Accede a la API:

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

🧱 Estructura del proyecto
bash
Copy code
app/
  main.py           # Inicializa la app FastAPI
  routers/          # posts.py, users.py, auth.py, votes.py
  models.py         # Tablas SQLModel (Posts, Users, Votes)
  schemas.py        # Pydantic models (requests/responses)
  database.py       # Conexión y sesión a PostgreSQL
  oauth2.py         # Creación y validación de JWT
  utils.py          # Hashing (Argon2)
alembic/
  env.py
  versions/         # Migraciones versionadas
requirements.txt
⚙️ Stack y decisiones técnicas
FastAPI + SQLModel → validación automática y ORM tipado.

PostgreSQL + Alembic → persistencia estable y migraciones reproducibles.

OAuth2 + JWT → autenticación segura con tokens.

Argon2 (pwdlib) → cifrado robusto de contraseñas.

pydantic-settings → gestión limpia de configuración (.env).

CORS → habilitado para entorno local.

🔑 Endpoints principales
Método	Ruta	Descripción	Auth
POST	/users	Crear usuario	❌
POST	/login	Obtener token JWT	❌
GET	/posts	Listar posts públicos	❌
POST	/posts	Crear post	✅
PUT	/posts/{id}	Actualizar post	✅
DELETE	/posts/{id}	Eliminar post	✅
POST	/votes	Votar / quitar voto	✅

Autenticación:

makefile
Copy code
Authorization: Bearer <access_token>
🧬 Migraciones Alembic
bash
Copy code
alembic upgrade head         # aplica migraciones
alembic revision -m "msg"    # genera una nueva migración
alembic downgrade -1         # revierte una versión
En producción usa solo Alembic; no dependas de SQLModel.metadata.create_all().

🐳 Docker (opcional)
Ejemplo básico de docker-compose.yml:

yaml
Copy code
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://app:app@db:5432/appdb
      SECRET_KEY: change_me
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    depends_on:
      - db
    ports:
      - "8000:8000"

volumes:
  db_data:
bash
Copy code
docker compose up -d
🧪 Próximos pasos
Añadir tests con pytest.

Contenerizar completamente (Dockerfile + Compose).

Crear datos seed para entornos de demo.

Ampliar documentación técnica en docs/GUIDE.md.

🩵 Troubleshooting
Problema	Causa probable	Solución
Error al conectar a DB	URL incorrecta o Postgres apagado	Revisa DATABASE_URL y conexión local
401 Unauthorized	Falta token o expirado	Renueva el JWT en /login
CORS bloquea peticiones	Peticiones desde otro origen	Añade origen en middleware CORS

📜 Licencia
MIT © 2025 [Tu nombre o alias]

