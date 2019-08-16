from Database import Database
from models.post import post

Database.initialize()
post=post(blog_id="123",title="Another great post",content="This is some sample content",author="GS")
post.save_to_mongo()