from django.http import HttpRequest
from db.models import UnderReview, Tag
from ninja import Schema

import config
import os

class Remove(Schema):
    hash: str

def get(request):
    if "token" not in request.COOKIES or request.COOKIES["token"] not in config.VALIDD_ADMONI_PASSWORDSD:
        return 400, {}

    post = UnderReview.objects.first()

    if isinstance(post, UnderReview):
        return {
            "any": True,
            "tags": [{"tag": tag.tag, "count": len(tag.posts)} for tag in Tag.objects.all()],
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
    obj = UnderReview.objects.get(
        file_hash=data.hash
    )

    os.remove(config.IMAGE_SAVE_PATH / f"review/{data.hash}{obj.file_extension}")
    obj.delete()

    return { "success": True }
