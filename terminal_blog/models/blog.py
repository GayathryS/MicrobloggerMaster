import uuid
import datetime
from models.post import post

class Blog(object):
	def _init_(self, author, title, description, idno=None):
		self.author=author
		self.title=title
		self.description=description
		self.id=uuid.uuid4().hex if idno is None else idno
	def new_post(self):
		title=input("Enter post title: ")
		content=input("Enter post content: ")
		date=input("Enter post date(in format DDMMYYYY): ")
		post=post(blog_id=self.idno,title=title,content=content,author=self.author,date=datetime.strptime(date,"%d%m%Y"))
		post.save_to_mongo()
	def get_posts(self):
		return post.from_blog(self.idno)
	def save_to_mongo(self):
		Database.insert(collection='blogs',data=self.json())
	def json(self):
		return{'author':self.author,'title':self.title,'description':self.description,'id':self.idno}
	def get_from_mongo(cls, idno):
		blog_data=Database.find_one(collection='blogs',data={'id':idno})
		return cls(author=blog_data['author'],title=blog_data['title'],description=blog_data['description'],id=blog_data['idno'])