from Core.models import Product, Category, Vendor, Wishlist, ProductImages, ProductReview, Generation


def default(request):
    generations = {}

    categories = Category.objects.all()
    for category in categories:
        generations[category.title] = []
        for generation in category.generation.all():
            generations[category.title].append(generation.title)

    return {
        'categories': categories,
        'generations': generations
    }