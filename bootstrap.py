"""Bootstrap script to initialize the app."""
import app

from auth.models import User
from catalog.models import Category, Item


def main():
    """Bootstrap script, run once before app usage."""
    print("Initiating engine...")
    app.db.create_all()

    user = User(username="firstUser", password="muypassword12",
                email="h@gmail.com")
    user.make_password()

    app.db.session.add(user)
    app.db.session.commit()

    category = Category(title="Computer stuff",
                        description="Add stuff about computers here")

    app.db.session.add(category)
    app.db.session.commit()

    item = Item(title="click me", link="http://www.google.com",
                author=1, category=1)

    app.db.session.add(item)
    app.db.session.commit()


if __name__ == "__main__":
    main()
