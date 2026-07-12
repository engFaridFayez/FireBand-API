from django.db import models

# Create your models here.
class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="event_categories/")
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="sub_categories/",null=True,blank=True)
    category = models.ForeignKey(EventCategory,on_delete=models.CASCADE,related_name="subcategories")
    min_members = models.PositiveIntegerField(default=5)
    max_members = models.PositiveIntegerField(default=40)

    def __str__(self):
        return self.name

class Rule(models.Model):
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="rules")
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
    class Meta:
        ordering = ["order"]

class DurationOption(models.Model):
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="duration_options")
    title = models.CharField(max_length=100) #ex: superset, set 
    minutes = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True,null=True)
    event_date = models.DateField()
    event_time = models.TimeField() # الساعه كام يعني 
    location = models.CharField(max_length=255)
    category = models.ForeignKey(EventCategory,on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.PROTECT)
    custom_sub_category = models.CharField(max_length=255,blank=True,null=True)
    duration = models.ForeignKey(DurationOption,on_delete=models.PROTECT)
    team_members = models.PositiveIntegerField()
    notes = models.TextField(blank=True)