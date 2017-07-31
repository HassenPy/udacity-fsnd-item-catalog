"""Catalog app models."""
from app import db


class Category(db.Model):
    """sqlalchemy Category model."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text())
    items = db.relationship("Item", back_populates="Category")

    def __init__(self, title, description):
        """Class constructor."""
        self.title = title
        self.description = description
        self.errors = {}
        self.validators = [
        ]

    def __unicode__(self):
        """Text representation of the Category class instance."""
        return '%s' % self.title

    def __repr__(self):
        """Printable representation of the Category class instance."""
        return "<Category(title='%r')>" % (self.title)


class Item(db.Model):
    """sqlalchemy Category model."""

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    link = db.Column(db.String(20))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship("Category", back_populates="Item")

    def __init__(self, title, link):
        """Class constructor."""
        self.title = title
        self.link = link
        self.errors = {}
        self.validators = [
        ]

    def __unicode__(self):
        """Text representation of the Item class instance."""
        return '%s' % self.title

    def __repr__(self):
        """Printable representation of the Item class instance."""
        return "<Item(title='%r')>" % (self.title)
