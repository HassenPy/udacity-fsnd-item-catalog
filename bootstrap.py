"""Bootstrap script to initialize the app."""
from app import db


def main():
    """Bootstrap script, run once before app usage."""
    print("Initiating engine...")
    db.create_all()


if __name__ == "__main__":
    main()
