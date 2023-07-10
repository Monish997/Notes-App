import sys

sys.path.insert(0, ".")
from notes import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
