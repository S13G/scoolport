from django.db import models

from apps.common.models import BaseModel


# Create your models here.


class FAQ(BaseModel):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()

    def __str__(self):
        return self.question
