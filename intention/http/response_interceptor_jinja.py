from ..role.intercepts_http_response import intercepts_http_response
from ..role.service import service
from .jinja_response import JinjaResponse
from .response_interceptor import ResponseInterceptor


@intercepts_http_response(JinjaResponse)
@service
class ResponseInterceptorJinja(ResponseInterceptor):
    pass
