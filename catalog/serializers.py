"""JSON serializers for the catalog app."""


class CommunitySerializer(object):
    """Minimal paginator to dict serializer."""

    def __init__(self, community):
        """PaginationSerializer constructor."""
        self.id = community.id
        self.title = community.title
        self.description = community.description

    def serialize(self):
        """Return dict representation of paginator."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }


class PickSerializer(object):
    """Pick object to dict serializer."""

    def __init__(self, pick):
        """PickSerializer constructor."""
        self.pick = pick

    def serialize(self):
        """Return dict representation of Pick."""
        return {
            "id": self.pick.id,
            "title": self.pick.title,
            "link": self.pick.link,
            "created": self.pick.created,
            "edited": self.pick.edited,
            "community": self.pick.community,
            "author": self.pick.author
        }
