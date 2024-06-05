from django.db import models

class Image(models.Model):
    post_id = models.IntegerField(unique=True, primary_key=True)
    file_hash = models.CharField(max_length=64, unique=True)
    file_extension = models.CharField(max_length=4)
    tags = models.JSONField(default=list, blank=True)
    timestamp = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.file_hash}{self.file_extension} ({len(self.tags)} tags)"

class Tag(models.Model):
    tag = models.TextField(unique=True, primary_key=True)
    posts = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return f"{self.tag} ({len(self.posts)} posts)"

class UnderReview(models.Model):
    file_hash = models.CharField(max_length=64, unique=True)
    file_extension = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f"{self.file_hash}{self.file_extension}"
