from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Agrupa toda la configuración sensible de la API cargada desde variables de entorno."""

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        # Indica a Pydantic qué archivo revisar si las variables no vienen del entorno.
        env_file = ".env"  # Le indico de donde coger las variables


# Instancia única que se importará desde cualquier módulo que necesite configuración.
settings = Settings()
