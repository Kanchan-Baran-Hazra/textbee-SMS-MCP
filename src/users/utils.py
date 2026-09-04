import time
import jwt
from pathlib import Path
from pwdlib import PasswordHash

base_dir = Path(__file__).resolve().parent.parent


PRIVATE_KEY = open(base_dir / "keys" / "private_key.pem", "r").read()

ISSUER = "http://localhost:9000"
AUDIENCE = "my-mcp-server"

password_hash = PasswordHash.recommended()


def hash_password(password: str):

    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
):

    return password_hash.verify(
        password,
        hashed_password,
    )


def create_access_token(
    user_id: str,
    username: str,
    scopes: list[str],
):

    now = int(time.time())

    payload = {
        "sub": str(user_id),
        "username": username,
        "scope": " ".join(scopes),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + 3600,
    }

    token = jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256",
    )

    return token


# if __name__ == "__main__":

#     token = create_token(
#         user_id="123",
#         client_id="alice",
#         scopes=["profile:read"],
#     )

#     print("\nJWT:\n")
#     print(token)
