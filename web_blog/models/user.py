import uuid

class User(object):
	def __init__(self, email,password,idno=None):
		self.email=email
		self.password=password
		self.id=uuid.uuid4().hex if idno is None else idno
	
	@classmethod
	def get_by_email(cls,email):
		data=database.find_one("users",{"email":email})
		if data is not None:
			return cls(**data)

	@classmethod
	def get_by_id(cls,idno):
		data=database.find_one("users",{"idno":idno})
		if data is not None:
			return cls(**data)
	
	@staticmethod
	def login_valid(email,password):
		user=User.get_by_email(email)
		if user is not None:
			return user.password==password
		return False
    
    @classmethod
	def register(cls,email,password):
		user=cls.get_by_email(email)
		if user is None:
			new_user=cls(email,password)
			new_user.save_to_mongo()
			session['email']=email
			return True
		else:
			return False
	
	def login(user_email):
		session['email']=user_email

	@staticmethod
	def logout():
		session['email']=None
	
	def get_blogs(self):
		return blogs.find_by_author_id(self.idno)

	def new_blog(self,title,description):
		blog=blog(author=self.email,title=title,description=description,author_id=self.idno)
		blog.save_to_mongo()
    
    @staticmethod
	def new_post(blog_id,title, content,date):
		blog=blog.from_mongo(blog_id)
		bog.new_post(title=title,content=content,date=date)

	
	def json(self):
		return{"email":self.email,"idno":self.idno,"password":self.password}
	
	def save_to_mongo(self):
		database.insert("users",self.json())
