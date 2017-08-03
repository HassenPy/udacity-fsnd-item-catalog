"""Catalog app models."""
import bleach
from slugify import slugify
from datetime import datetime
from sqlalchemy.orm import reconstructor
from validators import url
from validators.utils import ValidationFailure

from app import db


class Category(db.Model):
    """sqlalchemy Category model."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    slug = db.Column(db.String(25), unique=True)
    description = db.Column(db.Text())

    def __init__(self, title, description):
        """Class constructor called only when creating an object."""
        self.title = bleach.clean(title)
        self.description = bleach.clean(description)
        self.slug = slugify(self.title)
        self.validators = [self.validate_title, ]
        self.errors = {}

    @reconstructor
    def query_reconstructor(self):
        """Reconstructor called when fetching query from db."""
        # check: http://docs.sqlalchemy.org/en/latest/orm/constructors.html
        self.errors = {}
        self.validators = [self.validate_title, ]

    def validate_title(self):
        """Title validator."""
        field = self.title
        errors = []

        if not (len(field) in range(3, 25)):
            errors.append(
                    "Title must be longer than 3 and "
                    "shorter than 25 characters"
            )

        if errors:
            self.errors["title"] = errors

    def is_valid(self):
        """Check if the values passed to the model are valid."""
        for validator in self.validators:
            validator()
        if self.errors:
            return False
        return True

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
    title = db.Column(db.String(70), unique=True)
    link = db.Column(db.String(1000))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, title, link, author, category,
                 created=None, edited=None):
        """Class constructor."""
        self.title = bleach.clean(title)
        self.link = bleach.clean(link)
        self.author = author
        self.category = category
        if not created:
            self.created = datetime.utcnow()
        if not edited:
            self.edited = datetime.utcnow()
        self.errors = {}
        self.validators = [
            self.validate_title,
            self.validate_link
        ]

    @reconstructor
    def query_reconstructor(self):
        """Reconstructor called when fetching query from db."""
        # check: http://docs.sqlalchemy.org/en/latest/orm/constructors.html
        self.errors = {}
        self.validators = [
            self.validate_title,
            self.validate_link
        ]

    def validate_title(self):
        """Title validator."""
        field = self.title
        errors = []

        if not (len(field) in range(5, 70)):
            errors.append(
                    "Title must be longer than 5 and "
                    "shorter than 70 characters"
            )

        if errors:
            self.errors["title"] = errors

    def validate_link(self):
        """Validate link using the python validators library."""
        field = self.link
        errors = []

        # kind of weird way of raising a validation error.
        if isinstance(url(field, public=True), ValidationFailure):
            errors.append(
                    "invalid link."
            )

        if errors:
            self.errors["link"] = errors

    def is_valid(self):
        """Check if the values passed to the model are valid."""
        for validator in self.validators:
            validator()
        if self.errors:
            return False
        return True

    def __unicode__(self):
        """Text representation of the Item class instance."""
        return '%s' % self.title

    def __repr__(self):
        """Printable representation of the Item class instance."""
        return "<Item(title='%r')>" % (self.title)
