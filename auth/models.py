"""sqlalchemy models that represent the authn/authz database."""
# from sqlalchemy.orm import validates
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from pyisemail import is_email

from app import db

# https://github.com/michaelherold/pyIsEmail
# http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html?highlight=validate#simple-validators


class User(db.Model):
    """Base user model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email, email1):
        """Class constructor."""
        self.username = username
        self.password = password
        self.email = email
        self.email1 = email1
        self.errors = {}
        self.validators = [
            self.validate_username,
            self.validate_password,
            self.validate_email
        ]

    def validate_username(self):
        """Username validator."""
        field = self.username
        errors = []

        if not str.isalnum(field):
            errors.append(
                    "username is not alphanumeric."
            )
        if not (len(field) in range(3, 13)):
            errors.append(
                    "username must be longer than 3 and "
                    "shorter than 12 characters"
            )

        if errors:
            self.errors["username"] = errors

    def validate_email(self):
        """Email validator."""
        field = self.email
        errors = []

        if not is_email(field, check_dns=True):
            errors.append(
                    "email is invalid."
            )
        if field != self.email1:
            errors.append(
                    "emails do not match."
            )
        if errors:
            self.errors["email"] = errors

    def validate_password(self):
        """Password validator."""
        field = self.password
        errors = []

        if len(field) < 8:
            errors.append(
                    "password must be at least 8 characters long."
            )
        if field == self.username:
            errors.append(
                    "Password cannot be the same as your username."
            )
        if errors:
            self.errors["password"] = errors

    def make_password(self):
        """Generate Argon2 hash of the provided password."""
        # ref: https://argon2-cffi.readthedocs.io/en/stable/api.html
        # Note: Argon2 adds a salt by default.
        ph = PasswordHasher()
        hash = ph.hash(self.password)
        self.password = hash

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        ph = PasswordHasher()
        try:
            # Note: The ph.verify doesn't return a False value, it's either
            #       True or it raises a VerifyMismatchError exception.
            ph.verify(self.password, password)
            return True
        except argon2_exceptions.VerifyMismatchError:
            return False

    def is_valid(self):
        """Check if the values passed to the model are valid."""
        for validator in self.validators:
            validator()
        if self.errors:
            return False
        return True

    def __unicode__(self):
        """Text representation of the User class instance."""
        return '%s' % self.username

    def __repr__(self):
        """Printable representation of the User class instance."""
        return "<User(username='%r')>" % (self.username)
