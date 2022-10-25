import uvicorn
import asyncio
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from ariadne import MutationType, make_executable_schema
from starlette.applications import Starlette
from starlette.routing import (Route, WebSocketRoute)


type_defs = """
  type Query {
    _unused: Boolean
  }

  type Message {
    sender: String
    message: String
  }

  type Mutation {
    send(sender: String!, message: String!): Boolean
  }

  type Subscription {
    message: Message
  }
"""

mutation = MutationType()
schema = make_executable_schema(type_defs, mutation)

graphql_handler = GraphQL(
  schema=schema,
  debug=True,
  introspection=True,
  websocket_handler=GraphQLTransportWSHandler(),
  logger="admin.graphql"
)

routes = [
 Route("/api/graphql", endpoint=graphql_handler, name="graphql"),
 WebSocketRoute("/api/subscriptions", endpoint=graphql_handler, name="graphqlws")
]

app = Starlette(routes=routes)


async def main():
    config = uvicorn.Config("main:app", port=8000, log_config="log.json", log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())