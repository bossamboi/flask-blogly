from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add users
eric = User(first_name='Eric', last_name='Sohng')
maurice = User(first_name='Maurice', last_name='Baez')

# Add posts

post_1 = Post(title='My blog', content='first blog', user_id=1)
post_2 = Post(title='My blog2', content='second blog', user_id=1)

# Add tags

tag_1 = Tag(name="Funny")
tag_2 = Tag(name="Crazy")

# Add new objects to session, so they'll persist
db.session.add(eric)
db.session.add(maurice)
db.session.add_all([post_1, post_2])
db.session.add_all([tag_1, tag_2])
db.session.commit()

#Populate posttag table

posttag_1 = PostTag(post_id = post_1.id, tag_id = tag_1.id)
posttag_2 = PostTag(post_id = post_2.id, tag_id = tag_2.id)

db.session.add(posttag_2)

# Commit--otherwise, this never gets saved!
db.session.commit()
