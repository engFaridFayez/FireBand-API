from slugify import slugify

def generate_unique_slug(instance, model, value):
    slug = slugify(value)
    unique_slug = slug
    counter = 1

    while model.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug