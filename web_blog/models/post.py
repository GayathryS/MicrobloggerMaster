import Database
class post(object):
	def _init_(self,blog_id,title,content,author,created_date,idno):
		self.blog_id=blog_id
		self.title=title
		self.content=content
		self.author=author
		self.created_date= created_date
		self.id= idno
	def save_to_mongo(self):
		Database.insert(collection='posts',data=self.json())
	def json(self):
		return{
		'id': self.idno,
		'blog_id': self.blog_id,
		'author': self.author,
		'content': self.content,
		'title' : self.title,
		'created_date': self.created_date
		}
	@staticmethod
	def from_mongo(idno):
		data=Database.find_one(collection='posts', data={'id':idno})

	@staticmethod
	def from_blog(idno):
		return[post for post in Database.find(collection='posts',query={'blog_id': idno})]