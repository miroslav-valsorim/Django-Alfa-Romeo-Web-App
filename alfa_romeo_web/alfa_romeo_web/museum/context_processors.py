from .models import MuseumCategory
from ..history.models import HistoryCategory


def navbar_objects(request):
    museum_categories = MuseumCategory.objects.all()
    history_categories = HistoryCategory.objects.filter(is_active=True)
    return {
        'museum_categories': museum_categories,
        'history_categories': history_categories,
    }
