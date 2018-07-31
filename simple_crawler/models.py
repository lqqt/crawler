from django.db import models

# Create your models here.


class FullWebsite(models.Model):
    content = models.TextField("Content")

    def __str__(self):
        return self.content[:100]


class Element(models.Model):
    title = models.CharField(max_length=100)
    address = models.URLField()
    describtion = models.CharField(max_length=300)
    content = models.ForeignKey(FullWebsite, on_delete=models.CASCADE)

    def __str__(self):
        return self.title