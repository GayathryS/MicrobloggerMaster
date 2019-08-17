import uuid
import datetime
from models.post import post

class Blog(object):
	def _init_(self, author, title, description,author_id, idno=None):
		self.author=author
		self.author_id=author_id
		self.title=title
		self.description=description
		self.id=uuid.uuid4().hex if idno is None else idno
	def new_post(self,title,content,date):
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
		return{'author':self.author,'author_id':self.author_id,'title':self.title,'description':self.description,'id':self.idno}
	def get_from_mongo(cls, idno):
		blog_data=Database.find_one(collection='blogs',data={'id':idno})
		return cls(**blog_data)

	def find_by_author_id(cls,author_id):
		blog=database.find(collection='blogs',query={'author_id':author_id})
		return [cls(**blog) for blog in blogs]
