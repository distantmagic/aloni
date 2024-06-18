from ..role.intercepts_http_response import intercepts_http_response
from .jinja_response import JinjaResponse
from .response_interceptor import ResponseInterceptor
from .text_response import TextResponse
from jinja2 import Environment


@intercepts_http_response(response_class=JinjaResponse)
class JinjaResponseInterceptor(ResponseInterceptor[JinjaResponse]):
    def __init__(
        self,
        environment: Environment,
    ):
        ResponseInterceptor.__init__(self)

        self.environment = environment

    async def intercept(self, response: JinjaResponse) -> TextResponse:
        template = self.environment.get_template(response.template_filename)

        return TextResponse(
            content=await template.render_async(),
            content_type="text/html",
            status=response.get_status(),
        )
