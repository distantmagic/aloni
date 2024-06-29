import json

from ..role.intercepts_http_response import intercepts_http_response
from .json_response import JsonResponse
from .response_interceptor import ResponseInterceptor
from .text_response import TextResponse
from jinja2 import Environment


@intercepts_http_response(response_class=JsonResponse)
class JsonResponseInterceptor(ResponseInterceptor[JsonResponse]):
    async def intercept(self, response: JsonResponse) -> TextResponse:
        return TextResponse(
            content=json.dumps(response.data),
            content_type="application/json",
            status=response.get_status(),
        )
