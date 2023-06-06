from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50, blank=True)
    
    def __str__(self) -> str:
        return self.title
