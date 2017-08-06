"""Catalog app models."""
import bleach
from slugify import slugify
from datetime import datetime
from sqlalchemy.orm import reconstructor
from validators import url
from validators.utils import ValidationFailure

from app import db
from auth.models import User


class Community(db.Model):
    """sqlalchemy model and validation for the community table."""

    __tablename__ = 'community'

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

    @property
    def absolute_path(self):
        """Return domain independant absolute path."""
        return "/community/%d/" % (self.id)

    def __unicode__(self):
        """Text representation of the Community class instance."""
        return '%s' % self.title

    def __repr__(self):
        """Printable representation of the Community class instance."""
        return "<Community(title='%r')>" % (self.title)


class Pick(db.Model):
    """sqlalchemy model and validation for the Pick table."""

    __tablename__ = 'pick'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    link = db.Column(db.String(1000))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    community = db.Column(db.Integer, db.ForeignKey('community.id'))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, title, link, author, community,
                 created=None, edited=None):
        """Class constructor."""
        self.title = bleach.clean(title)
        self.link = bleach.clean(link)
        self.author = author
        self.community = community
        if not created:
            self.created = datetime.utcnow()
        if not edited:
            self.edited = datetime.utcnow()
        self.errors = {}
        self.validators = [
            self.validate_title,
            self.validate_link,
            self.validate_author,
            self.validate_community
        ]

    @reconstructor
    def query_reconstructor(self):
        """Reconstructor called when fetching query from db."""
        # check: http://docs.sqlalchemy.org/en/latest/orm/constructors.html
        self.errors = {}
        self.validators = [
            self.validate_title,
            self.validate_link,
            self.validate_author,
            self.validate_community
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
                    "invalid link"
            )

        if errors:
            self.errors["link"] = errors

    def validate_author(self):
        """Author fk validator."""
        field = self.author
        errors = []

        user = User.query.get(field)
        if not user:
            errors.append("Author doesn't exist")

        if errors:
            self.errors["author"] = errors

    def validate_community(self):
        """Community fk validator."""
        field = self.community
        errors = []

        community = Community.query.get(field)
        if not community:
            errors.append("Community doesn't exist")

        if errors:
            self.errors["community"] = errors

    def is_valid(self):
        """Check if the values passed to the model are valid."""
        for validator in self.validators:
            validator()
        if self.errors:
            return False
        return True

    def __unicode__(self):
        """Text representation of the Pick class instance."""
        return '%s' % self.title

    def __repr__(self):
        """Printable representation of the Pick class instance."""
        return "<Pick(title='%r')>" % (self.title)
