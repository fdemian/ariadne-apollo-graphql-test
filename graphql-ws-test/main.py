import uvicorn
import asyncio
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from ariadne import MutationType, SubscriptionType, make_executable_schema
from starlette.applications import Starlette
from starlette.routing import (Route, WebSocketRoute)
from message_subscriptions import (chat_resolver, chat_generator)

type_defs = """
  type Query {
    _unused: Boolean
  }

  type Message {
    text: String!
  }

  type Subscription {
    chatAdded: Message
  }
"""

subscription = SubscriptionType()
subscription.set_field("chatAdded", chat_resolver)
subscription.set_source("chatAdded", chat_generator)

schema = make_executable_schema(type_defs, subscription)


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
