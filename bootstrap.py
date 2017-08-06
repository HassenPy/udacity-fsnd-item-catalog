"""Bootstrap script to initialize the app."""
from app import create_app

from auth.models import User
from catalog.models import Community, Pick


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

    community = Community(title="Computer stuff",
                          description="Add stuff about computers here")
    db.session.add(community)
    db.session.commit()

    community = Community(title="Life hacks",
                          description="Add life hack links here")
    db.session.add(community)
    db.session.commit()

    pick = Pick(
        title="Principles Of Minimalist Web Design, With Examples",
        link=("https://www.smashingmagazine.com/2010/05/principles-of-"
              "minimalist-web-design-with-examples/"),
        author=2, community=1
    )
    db.session.add(pick)
    pick1 = Pick(
        title="Testing Flask Apps, Something that is untested is broken",
        link="http://flask.pocoo.org/docs/0.12/testing/",
        author=1, community=1
    )
    db.session.add(pick1)
    pick2 = Pick(
        title="Flask Application Factories",
        link="http://flask.pocoo.org/docs/0.12/patterns/appfactories/",
        author=2, community=1
    )
    db.session.add(pick2)
    pick3 = Pick(
        title="5 things designers wish their clients from hell knew",
        link=("https://medium.com/@KeiraBui/5-things-designers-wish-their"
              "-clients-from-hell-knew-dac7a4126a53"),
        author=1, community=2
    )
    db.session.add(pick3)
    pick4 = Pick(
        title=("Discover fundamentals of computer programming by playing a "
               "board game!"),
        link="http://www.c-jump.com/",
        author=2, community=2
    )
    db.session.add(pick4)
    pick5 = Pick(
        title="How to Scale Django: Beyond the Basics",
        link=("https://www.digitalocean.com/community/tutorials/how-to-"
              "scale-django-beyond-the-basics"),
        author=1, community=1)
    db.session.add(pick5)
    pick6 = Pick(
        title="Where To Start When You’ve Procrastinated On "
              "Your Goals For Too Long",
        link=("https://medium.com/personal-growth/where-to-start-when-youve"
              "-procrastinated-on-your-goals-for-too-long-ead87d0c91ba"),
        author=2, community=1
    )
    db.session.add(pick6)

    db.session.commit()


if __name__ == "__main__":
    app, db = create_app()
    bootstrap(app, db)
