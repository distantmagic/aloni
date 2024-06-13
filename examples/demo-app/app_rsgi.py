from intention import create_rsgi_handler

import intention_app

rsgi_handler = create_rsgi_handler(intention_app)


async def app(scope, proto):
    await rsgi_handler(scope, proto)
