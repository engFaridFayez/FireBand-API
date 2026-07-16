from django.db import models

# Create your models here.
class Show(models.Model):
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField()
    tag = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="shows/", blank=True)

    class Meta:
        ordering = ["date"]
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    accent = models.CharField(max_length=30)
    image = models.ImageField(upload_to="team/",blank=True)
    order = models.PositiveIntegerField(default=0)