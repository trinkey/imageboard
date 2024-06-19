from db.models import UnderReview, Tag, Image
from django.db import IntegrityError
from ninja import Schema

import config
import time
import os

from ..vars import Vars

class DelTag(Schema):
    tags: list[str]

class Approve(Schema):
    hash: str
    tags: list[str]

class Remove(Schema):
    hash: str

def get(request):
    if "token" not in request.COOKIES or request.COOKIES["token"] not in config.VALID_ADMIN_PASSWORDS:
        return 400, {}

    post = UnderReview.objects.first()

    if isinstance(post, UnderReview):
        def key(a):
            return a["tag"].lower()

        return {
            "any": True,
            "tags": sorted([{"tag": tag, "count": Vars.all_tags[tag]} for tag in Vars.all_tags], key=key),
            "post_info": {
                "hash": post.file_hash,
                "ext": post.file_extension
            }
        }

    else:
        return {
            "any": False,
            "tags": [],
            "post_info": {}
        }

def remove(request, data: Remove):
    if "token" not in request.COOKIES or request.COOKIES["token"] not in config.VALID_ADMIN_PASSWORDS:
        return 400, {}

    obj = UnderReview.objects.get(
        file_hash=data.hash
    )

    os.remove(config.IMAGE_SAVE_PATH / f"review/{data.hash}{obj.file_extension}")
    obj.delete()

    return {
        "success": True
    }

def del_tags(request, data: DelTag):
    if "token" not in request.COOKIES or request.COOKIES["token"] not in config.VALID_ADMIN_PASSWORDS:
        return 400, {}

    for i in data.tags:
        del Vars.all_tags[i]

        tag = Tag.objects.get(
            tag=i
        )

        for o in tag.posts:
            x = Image.objects.get(
                file_hash=o
            )

            x.tags.remove(o)
            x.save()

        tag.delete()

    return 200, {
        "success": True
    }

def approve(request, data: Approve):
    if "token" not in request.COOKIES or request.COOKIES["token"] not in config.VALID_ADMIN_PASSWORDS:
        return 400, {}

    try:
        rev = UnderReview.objects.get(
            file_hash=data.hash
        )

        os.rename(config.IMAGE_SAVE_PATH / f"review/{data.hash}{rev.file_extension}", config.IMAGE_SAVE_PATH / f"global/{data.hash}{rev.file_extension}")

        valid_tags = []

        for i in data.tags:
            try:
                tag = Tag.objects.get(
                    tag=i
                )

                tag.posts.append(data.hash)
                tag.save()

                Vars.all_tags[i] += 1

                valid_tags.append(i)

            except Tag.DoesNotExist:
                ...

        ext = rev.file_extension
        rev.delete()

        Image.objects.create(
            file_hash=data.hash,
            file_extension=ext,
            tags=valid_tags,
            timestamp=round(time.time())
        )

    except UnderReview.DoesNotExist:
        ...
    except IntegrityError:
        ...

    return {
        "success": True
    }
