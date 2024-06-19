from db.models import Tag

class Vars:
    all_tags = {}

for tag in Tag.objects.all():
    Vars.all_tags[tag.tag] = len(tag.posts)
