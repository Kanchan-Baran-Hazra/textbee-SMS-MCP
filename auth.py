# import time
# import jwt


# PRIVATE_KEY = open("private_key.pem", "r").read()

# ISSUER = "http://localhost:9000"
# AUDIENCE = "my-mcp-server"


# def create_token(
#     user_id: str,
#     client_id: str,
#     scopes: list[str],
# ):

#     now = int(time.time())

#     payload = {
#         "sub": user_id,
#         "client_id": client_id,
#         "scope": " ".join(scopes),

#         "iss": ISSUER,
#         "aud": AUDIENCE,

#         "iat": now,
#         "exp": now + 3600,
#     }

#     token = jwt.encode(
#         payload,
#         PRIVATE_KEY,
#         algorithm="RS256",
#     )

#     return token


# if __name__ == "__main__":

#     token = create_token(
#         user_id="123",
#         client_id="alice",
#         scopes=["profile:read"],
#     )

#     print("\nJWT:\n")
#     print(token)


import time
import sqlite3
import jwt

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash

PRIVATE_KEY = open("keys/private_key.pem").read()

ISSUER = "http://localhost:9000"
AUDIENCE = "my-mcp-server"

DB = "users.db"

password_hash = PasswordHash.recommended()

app = FastAPI()


class LoginRequest(BaseModel):
    username: str
    password: str


def get_db():
    return sqlite3.connect(DB)


def create_users():

    db = get_db()

    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            scopes TEXT NOT NULL
        )
    """)

    # Check if demo user exists
    cursor.execute("SELECT id FROM users WHERE username = ?", ("kanchan",))

    user = cursor.fetchone()

    if not user:

        hashed_password = password_hash.hash("1234")

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash, scopes)
            VALUES (?, ?, ?)
            """,
            ("kanchan", hashed_password, "profile:read"),
        )

    db.commit()
    db.close()


def create_token(
    user_id: int,
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

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256",
    )


@app.on_event("startup")
def startup():

    create_users()


@app.post("/login")
def login(data: LoginRequest):

    db = get_db()

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, username, password_hash, scopes
        FROM users
        WHERE username = ?
        """,
        (data.username,),
    )

    user = cursor.fetchone()

    db.close()

    # User doesn't exist
    if not user:

        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_id, username, stored_hash, scopes = user

    # Verify password
    if not password_hash.verify(data.password, stored_hash):

        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_scopes = scopes.split()

    token = create_token(
        user_id=user_id,
        username=username,
        scopes=user_scopes,
    )

    return {"access_token": token, "token_type": "bearer"}
