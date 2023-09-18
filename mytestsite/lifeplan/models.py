from django.db import models

# Create your models here.
class Day(models.Model):
        title = models.CharField(max_length=255)
        time_create = models.DateTimeField(auto_now_add=True)
        is_published = models.BooleanField(default=True)

        def __str__(self):
                return self.title