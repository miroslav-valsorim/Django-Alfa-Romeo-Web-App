from alfa_romeo_web.products.models import Category


def navbar_product_objects(request):
    product_categories = Category.objects.filter(is_active=True)

    # Exclude the category "tickets"
    product_categories = [category for category in product_categories if category.name != "Tickets"]

    return {
        'product_categories': product_categories,
    }
