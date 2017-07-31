"""Bootstrap script to initialize the app."""
import app

from auth.models import User
from catalog.models import Category, Item


def main():
    """Bootstrap script, run once before app usage."""
    print("Initiating engine...")
    app.db.create_all()

    user = User(username="user", password="12345678",
                email="h@gmail.com")
    user.make_password()
    app.db.session.add(user)
    app.db.session.commit()

    admin = User(username="admin", password="12345678",
                 email="h1@gmail.com", admin=True)
    admin.make_password()
    app.db.session.add(admin)
    app.db.session.commit()

    category = Category(title="Computer stuff",
                        description="Add stuff about computers here")

    app.db.session.add(category)
    app.db.session.commit()

    item = Item(title="click me1", link="http://www.google.com",
                author=1, category=1)
    app.db.session.add(item)
    item1 = Item(title="click me2", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item1)
    item2 = Item(title="click me3", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item2)
    item3 = Item(title="click me4", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item3)
    item4 = Item(title="click me5", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item4)
    item5 = Item(title="click me6", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item5)
    item6 = Item(title="click me7", link="http://www.google.com",
                 author=1, category=1)
    app.db.session.add(item6)

    app.db.session.commit()


if __name__ == "__main__":
    main()
