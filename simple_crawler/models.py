from django.db import models

# Create your models here.


class FullWebsite(models.Model):
    content = models.TextField("Content")

class Element(models.Model):
    address = models.URLField()
    describtion = models.CharField(max_length=300)
    content = models.ForeignKey(FullWebsite, on_delete=models.CASCADE)
