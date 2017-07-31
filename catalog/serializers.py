"""JSON serializers for the catalog app."""
from app.settings import Config


class ItemSerializer(object):
    """Minimal object to dict serializer."""

    def __init__(self, item):
        """ItemSerializer constructor."""
        self.title = item.title
        self.link = item.link
        self.author = item.author
        self.category = item.category

    def serialize(self):
        """Return dict representation of Item."""
        return {
            'title': self.title,
            'link': self.link,
            'author': self.author,
            'category': self.category
        }


class CategoryPageSerializer(object):
    """Minimal paginator to dict serializer."""

    def __init__(self, title, description, paginator):
        """PaginationSerializer constructor."""
        self.title = title
        self.description = description
        self.items = []
        for item in paginator.items:
            self.items.append(ItemSerializer(item).serialize())
        self.page = paginator.page
        self.next_page = paginator.next_num
        self.prev_page = paginator.prev_num

    def serialize(self):
        """Return dict representation of paginator."""
        return {
            'title': self.title,
            'description': self.description,
            'items': self.items,
            'page': self.page,
            'next_page': self.next_page,
            'prev_page': self.prev_page
        }


class CategoryListSerializer(object):
    """Minimal paginator to dict serializer."""

    def __init__(self, categories):
        """PaginationSerializer constructor."""
        self.categories = categories

    def serialize(self):
        """Return dict representation of paginator."""
        categories_serialized = []
        for category in self.categories:
            categories_serialized.append({
                'title': category.title,
                'location': '%s/catalog/category/%d' %
                                        (Config.domain, category.id)
            })
        print(categories_serialized)
        return categories_serialized
