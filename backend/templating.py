from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from ensure_file import ensure_file as ef
from db.models import Image, UnderReview, Tag
from django.core.handlers.wsgi import WSGIRequest

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
        files = request.FILES.getlist("file")
        if len(files) > 20:
            return HttpResponseRedirect("/submit?reason=too_many_files", status=302)

        content_types = request.POST["content-type"].split(',')
        if any(ct not in ["image/png", "image/jpeg", "image/gif", "video/mp4"] for ct in content_types):
            return HttpResponseRedirect("/submit?reason=type", status=302)

        for file, content_type in zip(files, content_types):
            raw_data: bytes = file.read()
            file_hash: str = hashlib.sha256(raw_data).hexdigest()

            if len(raw_data) > 1024 * 1024 * 20:  # 20mb
                continue

            if not validate_image(raw_data, content_type):
                continue

            try:
                Image.objects.get(file_hash=file_hash)
                continue
            except Image.DoesNotExist:
                pass

            try:
                UnderReview.objects.get(file_hash=file_hash)
            except UnderReview.DoesNotExist:
                UnderReview.objects.create(
                    file_hash=file_hash,
                    file_extension=CONTENT_TYPE_MAP[content_type]
                )

            ef(config.IMAGE_SAVE_PATH / f"review/{file_hash}{CONTENT_TYPE_MAP[content_type]}", default_value=raw_data)

        return HttpResponseRedirect("/submit?reason=success", status=302)

    return render_template(
        request, "submit.html",
        TITLE=f"Submit - {config.SITE_NAME}"
    )

def admin_page(request) -> HttpResponse:
    if "token" in request.COOKIES and request.COOKIES["token"] in config.VALIDD_ADMONI_PASSWORDSD:
        if request.method == "POST":
            try:
                Tag.objects.create(
                    tag=request.POST["tag"].lower().replace("+", "_").replace(" ", "_")
                )
            except IntegrityError:
                ...

        return render_template(request, "admin.html", TITLE=f"Admin - {config.SITE_NAME}")
    return render_template(request, "admin-login.html", TITLE=f"Admin Log in - {config.SITE_NAME}")

def find_duplicates(arrays: list[list[str]]) -> list[str]:
    if not arrays:
        return []

    sets = [set(arr) for arr in arrays]

    common_elements = sets[0]
    for s in sets[1:]:
        common_elements &= s

    return list(common_elements)

def search(request: WSGIRequest) -> HttpResponse:
    query = list(set([i for i in (request.GET["q"].split(" ") if "q" in request.GET else []) if i]))
    page = int(request.GET["p"]) if "p" in request.GET else 1

    if len(query):
        posts = []
        for i in query:
            try:
                posts.append(Tag.objects.get(
                    tag=i
                ).posts)
            except Tag.DoesNotExist:
                posts.append([])
                break

        valid = sorted(
            [Image.objects.get(file_hash=i) for i in find_duplicates(posts)],
            key=lambda img: img.post_id,
            reverse=True
        )[40 * (page - 1) : 40 * page]

    else:
        valid = Image.objects.all()[::-1][40 * (page - 1) : 40 * page]

    posts = []
    for i in valid:
        posts.append({
            "hash": i.file_hash,
            "ext": i.file_extension,
            "tags": " ".join(i.tags)
        })

    return render_template(
        request, "search.html",

        posts=posts,
        page=page,
        pages=[
            page - 5,
            page - 4,
            page - 3,
            page - 2,
            page - 1,
            page + 1,
            page + 2,
            page + 3,
            page + 4,
            page + 5
        ],
        query=" ".join(query)
    )

def tags(request: WSGIRequest) -> HttpResponse:
    output = []

    for i in Tag.objects.all().order_by("tag"):
        output.append({
            "tag": i.tag,
            "count": len(i.posts)
        })

    return render_template(
        request, "tags.html",

        tags=output
    )
