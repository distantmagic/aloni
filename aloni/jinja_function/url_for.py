from .jinja_function import JinjaFunction
from ..role.jinja_function import jinja_function


@jinja_function(name="url_for")
class UrlFor(JinjaFunction):
    def __call__(self, route_name: str) -> str:
        return route_name
