from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.auth import require_scopes


PUBLIC_KEY = open("src/keys/public_key.pem", "r").read()


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
def hello() -> str:
    return "Hello from MCP!"


@mcp.tool(
    auth=require_scopes("profile:read")
)
def get_profile() -> dict:

    return {
        "user_id": "123",
        "name": "Kanchan",
    }


@mcp.tool(
    auth=require_scopes("admin")
)
def admin_operation() -> str:

    return "🔥 Admin operation executed!"


if __name__ == "__main__":

    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
    )






























# from fastmcp import FastMCP
# from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
# from fastmcp.server.auth import require_scopes


# # Development-only tokens
# verifier = StaticTokenVerifier(
#     tokens={
#         "alice-token": {
#             "client_id": "alice",
#             "scopes": ["profile:read"],
#         },
#         "admin-token": {
#             "client_id": "admin",
#             "scopes": ["profile:read", "admin"],
#         },
#     }
# )


# mcp = FastMCP(
#     name="Auth Demo",
#     auth=verifier,
# )


# @mcp.tool
# def hello() -> str:
#     """A basic authenticated tool."""
#     return "Hello! You are authenticated."


# @mcp.tool(auth=require_scopes("profile:read"))
# def get_profile() -> dict:
#     """Get the user's profile."""
#     return {
#         "name": "Kanchan",
#         "role": "user",
#     }


# @mcp.tool(auth=require_scopes("admin"))
# def admin_operation() -> str:
#     """An admin-only operation."""
#     return "🔥 Admin operation executed!"


# if __name__ == "__main__":
#     mcp.run(
#         transport="http",
#         host="127.0.0.1",
#         port=8000,
#     )






















# from fastmcp import FastMCP
# from fastmcp.server.auth import AccessToken, TokenVerifier


# class MyTokenVerifier(TokenVerifier):

#     async def verify_token(self, token: str) -> AccessToken | None:

#         # Our intentionally simple learning token
#         if token == "secret123":
#             return AccessToken(
#                 token=token,
#                 client_id="my-client",
#                 scopes=["profile:read"],
#                 expires_at=None,
#             )

#         return None


# auth = MyTokenVerifier()

# mcp = FastMCP(
#     name="Authenticated MCP",
#     auth=auth,
# )


# @mcp.tool()
# def public_tool() -> str:
#     return "Anyone can use this tool."


# @mcp.tool()
# def profile_tool() -> dict:
#     return {
#         "user_id": 123,
#         "name": "Kanchan",
#         "role": "user",
#     }


# if __name__ == "__main__":
#     mcp.run(
#         transport="http",
#         host="127.0.0.1",
#         port=8000,
#     )




























# from fastmcp import FastMCP
# from starlette.requests import Request
# from starlette.responses import PlainTextResponse

# mcp = FastMCP(
#     "DataAnalysis",
#     instructions="Provides tools for analyzing numerical datasets. Start with get_summary() for an overview.",
# )

# @mcp.tool
# def greet(name: str) -> str:
#     return f"Hello, {name}!"

# @mcp.tool
# def multiply(a: float, b: float) -> float:
#     """Multiplies two numbers together."""
#     return a * b

# @mcp.resource("data://config")
# def get_config() -> dict:
#     return {"theme": "dark", "version": "1.0"}


# @mcp.prompt
# def analyze_data(data_points: list[float]) -> str:
#     formatted_data = ", ".join(str(point) for point in data_points)
#     return f"Please analyze these data points: {formatted_data}"


# @mcp.custom_route("/health", methods=["GET"])
# async def health_check(request: Request) -> PlainTextResponse:
#     return PlainTextResponse("OK")









# from prefab_ui.app import PrefabApp
# from prefab_ui.components import Column, Heading, Text, Badge, Row,Badge, Card, CardContent, CardHeader, CardTitle, Row, Text
# from fastmcp import FastMCP

# mcp = FastMCP("My MCP Server")


# @mcp.tool(app=True)
# def greet(name: str) -> PrefabApp:
#     """Greet someone with a visual card."""
    # with Column(gap=4, css_class="p-6") as view:
    #     Heading(f"Hello, {name}!")
    #     with Row(gap=2, align="center"):
    #         Text("Status")
    #         Badge("Greeted", variant="success")

    # with Card(css_class="w-48") as view:
    #     with CardHeader():
    #         with Row(gap=2):
    #             CardTitle("API Server")
    #             Badge("Healthy", variant="success")
    #     with CardContent():
    #         Text("Uptime: 99.97%")

    # return PrefabApp(view=view)



# if __name__ == "__main__":
#     mcp.run(transport="http", host="localhost", port=9000)