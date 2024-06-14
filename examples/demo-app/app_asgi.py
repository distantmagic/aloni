from intention import create_asgi_handler

import demo_app

asgi_handler = create_asgi_handler(demo_app)


async def app(scope, receive, send):
    await asgi_handler(scope, receive, send)
