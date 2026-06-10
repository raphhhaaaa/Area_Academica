import os
from cryptography.fernet import Fernet

# Em produção, DEVE ser definida via variável de ambiente. Se não existir, gera e salva num arquivo temporário
key_file = ".secret.key"
if os.path.exists(key_file):
    with open(key_file, "r") as f:
        SECRET_KEY = f.read().strip()
else:
    SECRET_KEY = os.environ.get("SECRET_KEY", Fernet.generate_key().decode("utf-8"))
    with open(key_file, "w") as f:
        f.write(SECRET_KEY)

_fernet = Fernet(SECRET_KEY.encode("utf-8"))

def encrypt_password(password: str) -> str:
    """Criptografa uma senha em texto claro."""
    if not password:
        return ""
    return _fernet.encrypt(password.encode("utf-8")).decode("utf-8")

def decrypt_password(encrypted_password: str) -> str:
    """Descriptografa uma senha."""
    if not encrypted_password:
        return ""
    return _fernet.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")
