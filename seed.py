from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
eric = User(first_name='Eric', last_name='Sohng')
maurice = User(first_name='Maurice', last_name='Baez')

# Add new objects to session, so they'll persist
db.session.add(eric)
db.session.add(maurice)

# Commit--otherwise, this never gets saved!
db.session.commit()