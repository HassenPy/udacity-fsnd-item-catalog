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

    item = Item(
        title="Principles Of Minimalist Web Design, With Examples",
        link=("https://www.smashingmagazine.com/2010/05/principles-of-"
              "minimalist-web-design-with-examples/"),
        author=2, category=1
    )
    db.session.add(item)
    item1 = Item(
        title="Testing Flask Apps, Something that is untested is broken",
        link="http://flask.pocoo.org/docs/0.12/testing/",
        author=1, category=1
    )
    db.session.add(item1)
    item2 = Item(
        title="Flask Application Factories",
        link="http://flask.pocoo.org/docs/0.12/patterns/appfactories/",
        author=2, category=1
    )
    db.session.add(item2)
    item3 = Item(
        title="5 things designers wish their clients from hell knew",
        link=("https://medium.com/@KeiraBui/5-things-designers-wish-their"
              "-clients-from-hell-knew-dac7a4126a53"),
        author=1, category=2
    )
    db.session.add(item3)
    item4 = Item(
        title=("Discover fundamentals of computer programming by playing a "
               "board game!"),
        link="http://www.c-jump.com/",
        author=2, category=2
    )
    db.session.add(item4)
    item5 = Item(
        title="How to Scale Django: Beyond the Basics",
        link=("https://www.digitalocean.com/community/tutorials/how-to-"
              "scale-django-beyond-the-basics"),
        author=1, category=1)
    db.session.add(item5)
    item6 = Item(
        title="Where To Start When You’ve Procrastinated On "
              "Your Goals For Too Long",
        link=("https://medium.com/personal-growth/where-to-start-when-youve"
              "-procrastinated-on-your-goals-for-too-long-ead87d0c91ba"),
        author=2, category=1
    )
    db.session.add(item6)

    db.session.commit()


if __name__ == "__main__":
    app, db = create_app()
    bootstrap(app, db)
