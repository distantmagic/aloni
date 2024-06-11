from ..role import intercepts_http_response, singleton
from .jinja_template import JinjaTemplate
from .response_interceptor import ResponseInterceptor


@intercepts_http_response(JinjaTemplate)
@singleton
class ResponseInterceptorJinja(ResponseInterceptor):
    pass
