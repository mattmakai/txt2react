from django.template.defaultfilters import slugify

def create_slug(cls, unslugged):
    trial_slug = slugify(unslugged)
    if trial_slug == '':
        # set a default value in case of empty string
        trial_slug = slugify(cls.__name__) 
    slug = trial_slug
    count = 0
    while(cls.objects.filter(slug=slug).count() > 0):
        count += 1
        slug = trial_slug + str(count)
    return slug

