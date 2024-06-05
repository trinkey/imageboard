from django.contrib import admin
from django.urls import include, path
from db.models import Image, UnderReview, Tag
from backend.templating import simple_return, submit_file, admin_page, search, tags

admin.site.register(Image)
admin.site.register(UnderReview)
admin.site.register(Tag)

urlpatterns = [
    path("api/", include("backend.api")),

    path("", simple_return("index.html")),
    path("tags/", tags),
    path("admin/", admin_page),
    path("search/", search),
    path("submit/", submit_file),
    path("submitted/", simple_return("submitted.html")),

    path("django-admin/", admin.site.urls)
]

# handler404 = "backend.templating._404"
# handler500 = "backend.templating._500"
