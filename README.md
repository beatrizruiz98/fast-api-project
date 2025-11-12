# FastAPI Project – Guía de Uso

Documentación de cómo está construida la API, qué decisiones técnicas se tomaron y cómo volver a ponerla en marcha desde cero.

---

## ¿Qué problema resuelve?

Es una API REST para publicar posts, votar contenido y gestionar usuarios. La autenticación se basa en JWT (OAuth2 password flow) y cada recurso expone operaciones CRUD completas protegidas por permisos y relaciones en base de datos.

---

## Stack y decisiones clave

- **FastAPI + SQLModel**: aprovecha tipado de Pydantic y relaciones de SQLAlchemy sin perder la ergonomía de FastAPI (validaciones automáticas + documentación OpenAPI).
- **PostgreSQL + Alembic**: la estructura de tablas (`Posts`, `Users`, `Votes`) se maneja con migraciones versionadas para reproducir cualquier cambio estructural.
- **Autenticación JWT**: `app/oauth2.py` genera tokens firmados con `SECRET_KEY` y los verifica en cada endpoint protegido.
- **Gestión de configuración**: `pydantic-settings` carga las variables sensibles desde `.env`, evitando hardcodear secretos.
- **Hashing seguro**: `pwdlib` (Argon2) cifra contraseñas antes de persistirlas.
- **CORS**: `FastAPI` incluye un middleware que permite peticiones desde `localhost` o la IP local definida en `app/main.py`.

---

## Mapa rápido de carpetas

```
app/
  main.py           # crea app FastAPI y registra routers
  config.py         # Settings (BaseSettings) lee .env
  database.py       # engine y Session factory
  models.py         # tablas SQLModel (Posts, Users, Votes)
  schemas.py        # modelos Pydantic para requests/responses
  routers/          # posts, users, auth, votes
  oauth2.py         # creación y verificación de JWT
  utils.py          # hashing y verificación de contraseñas
alembic/            # migraciones versionadas
requirements.txt    # dependencias exactas
```

---

## Requisitos previos

- Python 3.11+
- PostgreSQL accesible (local o remoto)
- Entorno virtual recomendado (`python -m venv venv`)
- Opcional: herramienta como `just`, `make` o `docker` si luego se automatiza

---

## Variables de entorno

Crea un archivo `.env` en la raíz (está excluido del control de versiones):

---

## Instalación paso a paso

1. **Clonar o descargar** el repositorio.
2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar la base de datos**: crea la BD indicada en tu `.env`.

---

## Migraciones con Alembic

El historial está en `alembic/versions`. Comandos útiles:

```bash
alembic upgrade head      # aplica todas las migraciones
alembic revision -m "msg" # genera un nuevo archivo en versions/
alembic downgrade -1      # vuelve un paso atrás
```

> Al ejecutar `uvicorn`, `SQLModel.metadata.create_all()` en `main.py` puede crear tablas en blanco (útil en desarrollo). En entornos reales, usa solo Alembic para mantener el versionado bajo control.

---

## Ejecutar la API

```bash
uvicorn app.main:app --reload  // fastapi dev --host 0.0.0.0 --pot 8000
```

Con eso tendrás:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
- Endpoint de salud: `GET /`

---

## Recorrido por los commits (modo tutorial)

1. **`ca48ca5` – Primer commit**: estructura base de FastAPI.
2. **`d5839b2` – Posts CRUD**: modelos, esquemas y rutas para publicar contenido.
3. **`c0b5eee` – Usuarios**: creación de usuarios, hashing de contraseñas y esquemas separados (`UserIn`, `UserOut`).
4. **`fe4ae54` – Routers modulares**: separación en `app/routers` con prefijos y tags.
5. **`1b4e9d5` y `4cd95bb` – Autenticación JWT**: login, generación y verificación de tokens.
6. **`43d0bc2` – Dependencia `get_current_user`**: todos los endpoints sensibles ahora validan el token automáticamente.
7. **`39226f5` – Relaciones Post ↔ User**: claves foráneas + restricciones de propietarios.
8. **`66f62dc` – Query params**: paginación y búsqueda en `GET /posts`.
9. **`43b757f` – Variables de entorno**: `Settings` centraliza configuración sensible.
10. **`8ec1319` – Votos**: join entre `Posts` y `Votes` para devolver conteos en cada respuesta.
11. **`06d0df7` – Alembic**: reaplicación de migraciones para mantener la base sin drift.
12. **`67929a7` – CORS**: apertura controlada para pruebas locales.

Usa esta cronología si necesitas rearmar la app o contar la historia en una documentación más larga.

---

## Flujo típico de uso

1. **Crear usuario**  
   `POST /users` con JSON `{"email": "...", "password": "...", "phone_number": "..."}`.
2. **Iniciar sesión**  
   `POST /login` con `form-data` (`username` = email). Respuesta: `access_token`.
3. **Consumir endpoints protegidos**  
   Incluye `Authorization: Bearer <token>` en:
   - `POST /posts` (crear)
   - `PUT /posts/{id}` y `DELETE /posts/{id}` (solo dueño)
   - `POST /votes` (dir=1 crea, dir=0 elimina)
4. **Listar contenido público**  
   `GET /posts?limit=10&skip=0&search=texto` es público, pero `GET /posts/{id}` valida propiedad.

Ejemplo rápido con `httpie`:

```bash
http POST :8000/users email=demo@mail.com password=123456
http -f POST :8000/login username=demo@mail.com password=123456
http POST :8000/posts title="Hola" content="Mi primer post" "Authorization:Bearer <token>"
```

---

## Buenas prácticas y próximos pasos

- Añadir tests con `pytest` (routers y auth).
- Contenerizar con Docker Compose (app + Postgres) para despliegues repetibles.
- Automatizar la creación de usuarios demo o datos seed para demos futuras.
- Extender documentación formal a partir de esta guía (diagramas, secuencias, etc.).

Con esto tienes una referencia rápida para levantar, depurar o seguir evolucionando tu primera API en FastAPI. ¡Éxitos con la documentación larga! 🎯

