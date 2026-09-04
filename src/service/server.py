from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.auth import require_scopes
from fastmcp.server.dependencies import get_access_token

from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db.models import User
from ..db.main import SessionLocal
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
PUBLIC_KEY = open(base_dir / "keys" / "public_key.pem").read()


verifier = JWTVerifier(
    public_key=PUBLIC_KEY,
    issuer="http://localhost:9000",
    audience="my-mcp-server",
    algorithm="RS256",
)


mcp = FastMCP(
    name="JWT Auth Demo",
    auth=verifier,
)


@mcp.tool
def hello():

    token = get_access_token()

    return {
        "message": "Hello!",
        "user_id": token.claims.get("sub"),
        "username": token.claims.get("username"),
    }


@mcp.tool(
    auth=require_scopes("user")
)
def get_profile():

    # Get verified JWT
    token = get_access_token()

    # Get user ID from JWT
    user_id = token.claims.get("sub")

    if not user_id:
        return {
            "error": "User ID missing from token"
        }

    # Open database session
    db: Session = SessionLocal()

    try:

        # Find authenticated user
        user = (
            db.query(User)
            .filter(
                User.id == int(user_id)
            )
            .first()
        )

        if not user:

            return {
                "error": "User not found"
            }

        return {
            "id": user.id,
            "username": user.username,
            "scopes": user.scopes.split(),
        }

    finally:

        db.close()



@mcp.tool()
def send_sms(
    recipient: str,
    message: str,
) -> dict:
    """
    Send an SMS to a phone number using TextBee.
    """

    token = get_access_token()

    user_id = int(token.claims["sub"])

    db = SessionLocal()

    try:
        stmt = select(User).where(User.id == user_id)

        user = db.scalar(stmt)

        if not user:
            raise ValueError("User not found")

        # Now you have the authenticated user
        print(user.username)

        # Send SMS here...

        return {
            "success": True,
            "message": "SMS sent successfully",
        }

    finally:
        db.close()


@mcp.tool(
    auth=require_scopes("admin")
)
def admin_operation():

    token = get_access_token()

    return {
        "message": "Admin operation allowed.",
        "user_id": token.claims.get("sub"),
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)