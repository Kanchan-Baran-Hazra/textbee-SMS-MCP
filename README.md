# 📱 FastMCP SMS Server

A production-oriented **Model Context Protocol (MCP) server** built with **FastMCP**, **JWT authentication**, **SQLAlchemy**, and the **TextBee SMS API**.

This project demonstrates how an MCP server can authenticate users, identify the authenticated user from a JWT, access user-specific data through SQLAlchemy, and expose SMS functionality as an MCP tool.

---

## ✨ Features

* 🔌 FastMCP server
* 🔐 JWT authentication with **RS256**
* 🔑 Public/private RSA key verification
* 👤 User registration and login
* 🗄️ SQLAlchemy database integration
* 🎫 Access token based authentication
* 🧑‍💻 Authenticated user identification using JWT `sub`
* 📱 Send SMS through TextBee
* 🔒 User-specific API credentials
* 🤖 MCP client support
* 🖥️ Claude Desktop integration
* ⚡ FastAPI authentication server

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Claude Desktop   │
                    │     MCP Client      │
                    └──────────┬──────────┘
                               │
                               │ MCP
                               ▼
                    ┌─────────────────────┐
                    │    FastMCP Server   │
                    │                     │
                    │  JWT Verification   │
                    │  MCP Tools         │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌─────────────┐       ┌──────────────┐
             │  SQLAlchemy │       │   TextBee    │
             │  Database   │       │   SMS API    │
             └─────────────┘       └──────────────┘
                    ▲
                    │
                    │ user_id
                    │
             ┌─────────────┐
             │ JWT Token   │
             │             │
             │ sub         │
             │ username    │
             │ scope       │
             │ iss         │
             │ aud         │
             └─────────────┘
```

---

# 📂 Project Structure

```text
mcp/
│
├── src/
│   │
│   ├── auth_server/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   │
│   ├── mcp_server.py
│   ├── mcp_database.py
│   └── client.py
│
├── keys/
│   ├── private_key.pem
│   └── public_key.pem
│
├── .gitignore
├── requirements.txt
└── README.md
```

> **Never commit `private_key.pem` or real API credentials to GitHub.**

---

# 🛠️ Technologies

| Technology   | Purpose                       |
| ------------ | ----------------------------- |
| Python       | Backend                       |
| FastMCP      | MCP server                    |
| FastAPI      | Authentication server         |
| SQLAlchemy   | Database ORM                  |
| SQLite       | Development database          |
| PyJWT        | JWT creation and verification |
| Cryptography | RSA cryptography              |
| Pwdlib       | Password hashing              |
| HTTPX        | HTTP requests                 |
| TextBee      | SMS delivery                  |

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Generate RSA Keys

This project uses **RS256**.

The authentication server signs JWTs using the private key:

```text
private_key.pem
```

The MCP server verifies them using:

```text
public_key.pem
```

Generate a key pair with OpenSSL:

```bash
openssl genrsa -out keys/private_key.pem 2048
```

Then:

```bash
openssl rsa \
  -in keys/private_key.pem \
  -pubout \
  -out keys/public_key.pem
```

On Windows PowerShell, the same commands can be run if OpenSSL is installed.

---

# 👤 Authentication Server

The authentication server provides:

```text
POST /register
POST /login
```

Start it with:

```powershell
uvicorn auth_server.main:app --port 9000
```

The authentication server will run at:

```text
http://127.0.0.1:9000
```

---

# 📝 Register a User

Example:

```powershell
curl.exe -X POST http://127.0.0.1:9000/register `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"kanchan\",\"password\":\"1234\"}'
```

Response:

```json
{
  "message": "User created successfully",
  "user_id": 1,
  "username": "kanchan"
}
```

---

# 🔑 Login

```powershell
curl.exe -X POST http://127.0.0.1:9000/login `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"kanchan\",\"password\":\"1234\"}'
```

Response:

```json
{
  "access_token": "YOUR_JWT_TOKEN",
  "token_type": "bearer"
}
```

The JWT contains claims such as:

```json
{
  "sub": "1",
  "username": "kanchan",
  "scope": "profile:read",
  "iss": "http://localhost:9000",
  "aud": "my-mcp-server",
  "iat": 1234567890,
  "exp": 1234571490
}
```

---

# 🔐 JWT Authentication

The MCP server uses an RSA public key to verify the JWT.

```python
verifier = JWTVerifier(
    public_key=PUBLIC_KEY,
    issuer="http://localhost:9000",
    audience="my-mcp-server",
    algorithm="RS256",
)
```

The authentication flow is:

```text
User
 │
 │ username + password
 ▼
Auth Server
 │
 │ signs JWT with private key
 ▼
Access Token
 │
 ▼
MCP Client
 │
 │ Bearer token
 ▼
FastMCP
 │
 │ verifies signature with public key
 ▼
MCP Tool
```

---

# 🗄️ SQLAlchemy Integration

The MCP tools use SQLAlchemy to access the database.

A database session is created using:

```python
db = SessionLocal()
```

Example:

```python
stmt = select(User).where(User.id == user_id)

user = db.scalar(stmt)
```

The session is closed after the operation:

```python
finally:
    db.close()
```

---

# 👤 Getting the Authenticated User

The MCP server does not need the client to provide a `user_id`.

Instead, the user ID comes from the verified JWT:

```python
token = get_access_token()

user_id = int(token.claims["sub"])
```

Then SQLAlchemy can find the user:

```python
stmt = select(User).where(User.id == user_id)

user = db.scalar(stmt)
```

This gives the MCP server the identity of the user who made the request.

---

# 📱 Send SMS Tool

The project exposes an MCP tool similar to:

```python
@mcp.tool()
def send_sms(
    recipient: str,
    message: str,
) -> dict:
    ...
```

The client only needs to provide:

```text
recipient
message
```

It does **not** need to provide:

```text
user_id
api_key
device_id
```

The server can determine the authenticated user from the JWT and retrieve that user's TextBee configuration from the database.

---

# 🤖 Claude Desktop

The MCP server can be connected to Claude Desktop as a local MCP server.

Example configuration:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "E:\\mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "E:\\mcp\\src\\mcp_server.py"
      ]
    }
  }
}
```

The configuration file is located at:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

After modifying the configuration, restart Claude Desktop.

Your MCP tools should then become available to Claude.

---

# ⚠️ Security

Do **not** commit secrets to GitHub.

Add the following to `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc

.env
.env.*

users.db

keys/private_key.pem

*.log
```

Never commit:

```text
private_key.pem
```

or:

```text
TextBee API keys
JWT secrets
database passwords
```

For production, store secrets in environment variables or a dedicated secrets manager.

---

# 🔄 Current Authentication Flow

```text
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       │ Login
       ▼
┌──────────────────┐
│  Auth Server     │
│    FastAPI       │
└────────┬─────────┘
         │
         │ RS256 JWT
         ▼
┌──────────────────┐
│   MCP Client     │
│ Claude / Custom  │
└────────┬─────────┘
         │
         │ Access Token
         ▼
┌──────────────────┐
│  FastMCP Server  │
│                  │
│ JWTVerifier      │
└────────┬─────────┘
         │
         │ Verified JWT
         ▼
┌──────────────────┐
│    MCP Tool      │
│                  │
│ get_access_token │
└────────┬─────────┘
         │
         │ sub → user_id
         ▼
┌──────────────────┐
│    SQLAlchemy    │
│                  │
│      User        │
└────────┬─────────┘
         │
         │ User credentials
         ▼
┌──────────────────┐
│     TextBee      │
│    SMS Gateway   │
└──────────────────┘
```

---

# 🧪 Development

Start the authentication server:

```powershell
uvicorn auth_server.main:app --port 9000
```

Start the MCP server:

```powershell
python mcp_server.py
```

For Claude Desktop, configure the MCP server using the `stdio` transport.

---

# 🚧 Roadmap

* [x] FastMCP server
* [x] FastAPI authentication server
* [x] User registration
* [x] User login
* [x] JWT authentication
* [x] RS256 signing
* [x] SQLAlchemy integration
* [x] Authenticated user lookup
* [x] TextBee SMS integration
* [x] Claude Desktop local integration
* [ ] OAuth 2.0 authorization server
* [ ] Multi-user TextBee credential management
* [ ] PostgreSQL support
* [ ] Refresh tokens
* [ ] Token revocation
* [ ] Production deployment
* [ ] HTTPS
* [ ] Rate limiting
* [ ] Audit logging

---

# 📚 What This Project Demonstrates

This project is primarily a learning and development example for understanding how the following technologies work together:

```text
MCP
 +
FastMCP
 +
JWT
 +
RS256
 +
FastAPI
 +
SQLAlchemy
 +
External APIs
```

The main goal is to demonstrate how an MCP tool can securely identify the authenticated user and perform user-specific operations.

---

# 📄 License

This project is available under the MIT License.

See `LICENSE` for details.

---

## ⭐ Contributing

Contributions, suggestions, and improvements are welcome.

If you find a bug or have an idea, feel free to open an issue or submit a pull request.
