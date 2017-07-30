"""Catalog app models."""
from app import db


class Catagory(db.Model):
    """sqlalchemy Category model."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text())
    items = db.relationship("item", back_populates="category")

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
    link = db.Column(db.Text())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    parent = db.relationship("category", back_populates="children")

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
