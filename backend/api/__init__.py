from django.urls import path
from ninja.renderers import BaseRenderer
from ninja import NinjaAPI

from .admin import get, remove, approve, del_tags

import json

response_schema = {
    200: dict,
    400: dict,
    404: dict,
    429: dict
}

class Renderer(BaseRenderer):
    media_type = "application/json"
    def render(self, request, data, *, response_status):
        try:
            return json.dumps(data)
        except TypeError:
            return data()

api = NinjaAPI(renderer=Renderer())

api.get("admin")(get)
api.post("admin")(approve)
api.patch("admin")(del_tags)
api.delete("admin")(remove)

urlpatterns = [
    path("", api.urls)
]
