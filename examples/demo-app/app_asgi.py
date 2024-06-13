from intention import create_asgi_handler

import intention_app

asgi_handler = create_asgi_handler(intention_app)


async def app(scope, receive, send):
    await asgi_handler(scope, receive, send)
