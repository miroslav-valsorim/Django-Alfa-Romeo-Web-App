from .models import MuseumCategory


def navbar_objects(request):
    categories = MuseumCategory.objects.all()  # Fetch the categories from the database
    return {'navbar_categories': categories}
