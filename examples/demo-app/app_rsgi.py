from intention import create_rsgi_handler

import demo_app

rsgi_handler = create_rsgi_handler(demo_app)


async def app(scope, proto):
    await rsgi_handler(scope, proto)
