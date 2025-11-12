from pwdlib import PasswordHash

# Instancia configurada con los parámetros recomendados de la librería.
password_hash = PasswordHash.recommended()


def get_password_hash(password):
    """Calcula un hash seguro para almacenar la contraseña en base de datos."""
    return password_hash.hash(password)


def verify(plain_password, hashed_password):
    """Comprueba si una contraseña en texto plano coincide con su hash."""
    return password_hash.verify(plain_password, hashed_password)
