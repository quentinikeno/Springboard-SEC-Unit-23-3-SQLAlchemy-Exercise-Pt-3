"""Seed file to make sample data for db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add sample users, posts, tags
hs = User(first_name='Han', last_name='Solo', image_url='https://tse1.mm.bing.net/th?id=OIP.cl5ZfOGYi6ZBgT5f-dQK6gHaIp&pid=Api')
pb = User(first_name='Pat', last_name='Butcher', image_url='https://static.wikia.nocookie.net/ghosts-bbc-2019/images/8/8e/Pat.jpg/revision/latest/scale-to-width-down/350?cb=20190527100310')
fp = User(first_name='Fio', last_name='Piccolo', image_url='https://image.tmdb.org/t/p/original/nAeCzilMRXvGaxiCpv63ZRVRVgh.jpg')

p1 = Post(title='Post 1', content='This is just some dummy content for Post 1.  Great stuff.', user_id='1')
p2 = Post(title='Post 2', content='This is just some dummy content for Post 2.  Great stuff.', user_id='2')
p3 = Post(title='Post 3', content='This is just some dummy content for Post 3.  Great stuff.', user_id='3')

db.session.add_all([hs, pb, fp, p1, p2, p3])
db.session.commit()

t1 = Tag(name="travel", posts_tags=[PostTag(post_id=p1.id), PostTag(post_id=p3.id)])
t2 = Tag(name="recipes", posts_tags=[PostTag(post_id=p2.id)])
t3 = Tag(name="coding", posts_tags=[PostTag(post_id=p2.id), PostTag(post_id=p3.id)])

db.session.add_all([t1, t2, t3])
db.session.commit()