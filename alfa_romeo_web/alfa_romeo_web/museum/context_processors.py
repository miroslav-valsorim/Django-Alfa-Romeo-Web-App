from .models import MuseumCategory
from ..history.models import HistoryCategory


def navbar_objects(request):
    museum_categories = MuseumCategory.objects.all()  # Fetch the categories from the database
    history_categories = HistoryCategory.objects.all()
    return {
        'museum_categories': museum_categories,
        'history_categories': history_categories,
    }
