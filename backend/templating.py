from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from ensure_file import ensure_file as ef
from db.models import Image, UnderReview, Tag

import config
import random
import hashlib

CONTENT_TYPE_MAP = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "video/mp4": ".mp4"
}

def render_template(request, file: str, **kwargs) -> HttpResponse:
    context = {
        "NAME": config.SITE_NAME,
        "DESCRIPTION": config.SITE_DESCRIPTION,
        "TITLE": config.SITE_NAME,

        "VERSION": str(random.random()),
        "TOTAL_POSTS": str(Image.objects.count())
    }

    for key, val in kwargs.items():
        context[key] = val

    return HttpResponse(
        loader.get_template(file).render(
            context, request
        )
    )

def simple_return(file: str):
    def x(request) -> HttpResponse:
        return render_template(request, file)

    x.__name__ = file
    return x

def validate_image(content: bytes, content_type: str) -> bool:
    if content_type == "image/png":
        return content[:8] == b"\x89PNG\r\n\x1a\n"
    elif content_type == "image/jpeg":
        return content[:2] == b"\xff\xd8"
    elif content_type == "image/gif":
        return content[:6] in (b"GIF87a", b"GIF89a")
    elif content_type == "video/mp4":
        return content[:4] in (b"\x00\x00\x00\x18", b"\x00\x00\x00\x20") and content[4:8] == b"ftyp"
    return False

def submit_file(request) -> HttpResponse:
    if request.method == "POST":
        content_type = request.POST["content-type"]
        if content_type not in ["image/png", "image/jpeg", "image/gif", "video/mp4"]:
            return HttpResponseRedirect("/submit?reason=type", status=302)

        raw_data: bytes = request.FILES["file"].read()
        file_hash: str = hashlib.sha256(raw_data).hexdigest()

        if len(raw_data) > 1024 * 1024 * 20: # 20mb
            return HttpResponseRedirect("/submit?reason=size")

        if not validate_image(raw_data, content_type):
            return HttpResponseRedirect("/submit?reason=invalid")

        try:
            Image.objects.get(file_hash=file_hash)
            return HttpResponseRedirect("/submit?reason=exists", status=302)
        except Image.DoesNotExist:
            ...

        try:
            UnderReview.objects.get(
                file_hash=file_hash
            )
        except UnderReview.DoesNotExist:
            UnderReview.objects.create(
                file_hash=file_hash,
                file_extension=CONTENT_TYPE_MAP[content_type]
            )

        ef(config.IMAGE_SAVE_PATH / f"review/{file_hash}{CONTENT_TYPE_MAP[content_type]}", default_value=raw_data)
        return HttpResponseRedirect("/submit?reason=success", status=302)

    return render_template(
        request, "submit.html",
        TITLE = f"Submit - {config.SITE_NAME}"
    )

def admin_page(request) -> HttpResponse:
    if "token" in request.COOKIES and request.COOKIES["token"] in config.VALIDD_ADMONI_PASSWORDSD:
        if request.method == "POST":
            try:
                Tag.objects.create(
                    tag=request.POST["tag"].lower().replace("+", "_")
                )
            except IntegrityError:
                ...

        return render_template(request, "admin.html", TITLE=f"Admin - {config.SITE_NAME}")
    return render_template(request, "admin-login.html", TITLE=f"Admin Log in - {config.SITE_NAME}")
