"""JSON serializers for the catalog app."""
# from flask import url_for


class ItemSerializer(object):
    """Minimal object to dict serializer."""

    def __init__(self, item):
        self.title = item.title
        self.link = item.link
        self.author = item.author
        self.category = item.category

    def serialize(self):
        return {
            'title': self.title,
            'link': self.link,
            'author': self.author,
            'category': self.category
        }
