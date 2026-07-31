from slugify import slugify
from django.core.mail import send_mail
from django.conf import settings


def send_test_email():
    send_mail(
        subject="Hello from Django",
        message="This email was sent successfully!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )



    
def generate_unique_slug(instance, model, value):
    slug = slugify(value)
    unique_slug = slug
    counter = 1

    while model.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug