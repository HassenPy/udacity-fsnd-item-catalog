"""JSON serializers for the catalog app."""
from app.settings import Config


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
                'location': '%s/catalog/category/%d/' %
                                        (Config.domain, category.id)
            })
        return categories_serialized


class ItemListSerializer(object):
    """Item object list to dict serializer."""

    def __init__(self, items):
        """ItemListSerializer constructor."""
        self.items = items

    def serialize(self):
        """Return dict representation of Items."""
        serialized = []
        for item in self.items:
            serialized.append({
                'title': item.title,
                'location': '%s/catalog/item/%d/' %
                            (Config.domain, item.id)
            })
        return serialized


class ItemSerializer(object):
    """Item object to dict serializer."""

    def __init__(self, item):
        """ItemSerializer constructor."""
        self.item = item

    def serialize(self):
        """Return dict representation of Item."""
        return {
            'title': self.item.title,
            'link': self.item.link,
            'created': self.item.created,
            'edited': self.item.edited,
            'author': '%s/user/%d' % (Config.domain, self.item.author,),
            'location': '%s/catalog/item/%d/' %
                        (Config.domain, self.item.id)
        }
