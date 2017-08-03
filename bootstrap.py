"""Bootstrap script to initialize the app."""
from app import create_app

from auth.models import User
from catalog.models import Category, Item


def bootstrap(app, db):
    """Bootstrap script, run once before app usage."""
    app.app_context().push()

    print("Initiating engine...")
    db.create_all()
    user = User(username="user", password="12345678",
                email="h@gmail.com")
    user.make_password()
    db.session.add(user)
    db.session.commit()

    admin = User(username="admin", password="12345678",
                 email="h1@gmail.com", admin=True)
    admin.make_password()
    db.session.add(admin)
    db.session.commit()

    category = Category(title="Computer stuff",
                        description="Add stuff about computers here")
    db.session.add(category)
    db.session.commit()

    category = Category(title="Life hacks",
                    description="Add life hack links here")
    db.session.add(category)
    db.session.commit()

    item = Item(title="admin item", link="http://www.google.com",
                author=2, category=1)
    db.session.add(item)
    item1 = Item(title="user item", link="https://www.youtube.com",
                 author=1, category=1)
    db.session.add(item1)
    item2 = Item(title="facebook", link="https://www.facebook.com",
                 author=2, category=2)
    db.session.add(item2)
    item3 = Item(title="twitter", link="https://www.twitter.com",
                 author=1, category=2)
    db.session.add(item3)
    item4 = Item(title="reddit", link="https://www.reddit.com",
                 author=2, category=1)
    db.session.add(item4)
    item5 = Item(title="gmail", link="https://www.gmail.com",
                 author=1, category=1)
    db.session.add(item5)
    item6 = Item(title="vimeo", link="https://www.vimeo.com",
                 author=2, category=1)
    db.session.add(item6)

    db.session.commit()


if __name__ == "__main__":
    app, db = create_app()
    bootstrap(app, db)
