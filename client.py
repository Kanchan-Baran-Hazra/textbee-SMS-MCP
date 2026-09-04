import asyncio

from fastmcp import Client


TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoia2FuY2hhbiIsInNjb3BlIjoicHJvZmlsZTpyZWFkIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo5MDAwIiwiYXVkIjoibXktbWNwLXNlcnZlciIsImlhdCI6MTc4ODU0NDgwMCwiZXhwIjoxNzg4NTQ4NDAwfQ.TeYzERGCK2Z15qvBC9gLfC7RT1Nj0OY-FP_5Zz5yZJ39LaX1jGthH0Kj_j3WzlYJnUPS3PUAfiHgH2hnT2K6DNfwjPqMZIfUTq9C8XGzF6AhSjs1U6THdzoiWWHLhuH9Lw3RU9riNiBjtK0THvWfJ-uE8coC72_LFJgGHMA5f2dSu7_K4KhrAyRBPrK5bQQ522ASfrhw1CiDm_oU7k_kuHH10ybGqcy6T_IEuHFE6HIwiO4y5D6jbFRvHd2fdAiNYgF9KCXj_HIfDINZVwgu90CetFXdGwaD1M7vwl5uEnNcsDEiF32WIgGPxt-sV7IP4eAxXY8Lij6T0OErmLBHxA"


async def main():

    async with Client(
        "http://127.0.0.1:8000/mcp",
        auth=TOKEN,
    ) as client:

        print("Connected!")

        result = await client.call_tool(
            "get_profile"
        )

        print(result)


asyncio.run(main())


























# import asyncio

# from fastmcp import Client


# async def main():

#     async with Client(
#         "http://127.0.0.1:8000/mcp",
#         auth="alice-token",
#     ) as client:

#         print("Connected!")

#         result = await client.call_tool(
#             "hello",
#             {}
#         )

#         print(result)

#         result = await client.call_tool(
#             "get_profile",
#             {}
#         )

#         print(result)

#         result = await client.call_tool(
#             "admin_operation",
#             {}
#         )

#         print(result)


# asyncio.run(main())





























# import asyncio
# from fastmcp import Client

# client = Client("http://localhost:9000/mcp")

# async def call_tool(name: str):
#     async with client:
#         result = await client.call_tool("multiply", {"a": 5.0, "b": 3.0})
#         print(result)

# asyncio.run(call_tool("Ford"))