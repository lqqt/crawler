from django.db import models

# Create your models here.


class FullWebsite(models.Model):
    content = models.TextField("Content", null=False, blank=True)

    def __str__(self):
        return self.content


class Element(models.Model):
    title = models.CharField(max_length=100)
    address = models.URLField()
    describtion = models.CharField(max_length=300)
    content = models.ForeignKey(FullWebsite, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title