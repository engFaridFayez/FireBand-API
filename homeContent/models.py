from django.db import models
from django.utils.text import slugify
from core.models import SubCategory

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


class GalleryImage(models.Model):
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="gallery_images")
    image = models.ImageField(upload_to="gallery/")
    title = models.CharField(max_length=255,blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order","-created_at"]
    
    def __str__(self):
        return self.title or f"Image #{self.pk}"
    
class Reel(models.Model):
    PLATFORM_CHOICES = [
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("tiktok", "TikTok"),
    ]



    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="reels",
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        allow_unicode=True,
    )
    description = models.TextField(
        blank=True,
    )
    artist = models.CharField(
        max_length=200,
        blank=True,
    )

    thumbnail = models.ImageField(
        upload_to="reels/thumbnails/",
        blank=True,
        null=True,
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
    )

    embed_url = models.URLField()

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                self.title,
                allow_unicode=True
            )[:200] or "reel"

            slug = base_slug
            counter = 2

            while Reel.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title