class Post(object):
	def _init_(self,blog_id,title,content,author,date,idno):
		self.blog_id=blog_id
		self.title=title
		self.content=content
		self.author=author
		self.created_date= date
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