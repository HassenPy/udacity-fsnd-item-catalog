"""JSON serializers for the catalog app."""


class CategorySerializer(object):
    """Minimal paginator to dict serializer."""

    def __init__(self, category):
        """PaginationSerializer constructor."""
        self.id = category.id
        self.title = category.title
        self.description = category.description

    def serialize(self):
        """Return dict representation of paginator."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }


class ItemSerializer(object):
    """Item object to dict serializer."""

    def __init__(self, item):
        """ItemSerializer constructor."""
        self.item = item

    def serialize(self):
        """Return dict representation of Item."""
        return {
            'id': self.item.id,
            'title': self.item.title,
            'link': self.item.link,
            'created': self.item.created,
            'edited': self.item.edited,
            'category': self.item.category,
            'author': self.item.author
        }
