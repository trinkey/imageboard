from django.contrib import admin
from django.urls import include, path
from db.models import Image, UnderReview, Tag
from backend.templating import simple_return, submit_file, admin_page, search, post

admin.site.register(Image)
admin.site.register(UnderReview)
admin.site.register(Tag)

urlpatterns = [
    path("", simple_return("index.html")),
    path("api/", include("backend.api")),
    path("tags/", simple_return("tags.html")),
    path("admin/", admin_page),
    path("search/", search),
    path("submit/", submit_file),
    path("submitted/", simple_return("submitted.html")),
    path("django-admin/", admin.site.urls),
    path("post/<str:hash>", post)
]

# handler404 = "backend.templating._404"
# handler500 = "backend.templating._500"
