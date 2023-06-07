from django.db import models


class Example(models.Model):
    """
    Example model
    """
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='examples')
    link = models.URLField(max_length=200)
    

    def __str__(self):
        return self.name
