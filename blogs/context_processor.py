
from  .models import Category

from socialPlatform.models import SocialPlatform


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_platforms(request):
    social_platforms = SocialPlatform.objects.all()
    return dict(social_platforms=social_platforms)