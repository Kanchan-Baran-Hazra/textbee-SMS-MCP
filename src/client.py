import asyncio
import httpx

from fastmcp import Client

AUTH_SERVER = "http://127.0.0.1:9000"
MCP_SERVER = "http://127.0.0.1:8000/mcp"


async def login():

    async with httpx.AsyncClient() as http:

        response = await http.post(
            f"{AUTH_SERVER}/users/login",
            json={
                "username": "kanchan",
                "password": "123456",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["access_token"]


async def main():

    # 1. Login
    token = await login()

    print("JWT received!")
    # print()

    # 2. Connect to MCP using JWT
    async with Client(
        MCP_SERVER,
        auth=token,
    ) as client:

        # 3. Call protected tool
        result = await client.call_tool(
            "send_sms",
            arguments={
                "recipient": "9679299095",
                "message": "Hello from my MCP client!",
            },
        )

        print("MCP response:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
