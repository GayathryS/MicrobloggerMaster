class menu(object):
	def _init_(self):
		self.user=input("Enter your author name")
		self.user_blog=None
		if self._user_has_account():
			print("welcome back {}".format(self.user))
		else:
			self._prompt_user_for_account()
		
	def _user_has_account(self):
		blog= Database.find_one('blogs',{'author':self.user}) is not None
		if blog is not None:
			self.user_blog=blog.from_mongo(blog['idno'])
			return True
		else:
			return False
	def _prompt_user_for_account(self):
		title=input("Enter blog title: ")
		description=input("Enter blog description")
		blog=Blog(author=self.user,title=title,description=description)
		blog.save_to_mongo()
		self.user_blog=blog

	
	def run_menu(self):
		read_or_write=input("Do you want to read(r) or write(w) blogs?")
		if(read_or_write=='r'):
			self._list_blogs()
			self._view_blogs()
		elif(read_or_write=='w'):
			self._prompt_write()
		else:
			print("Thank you for blogging")
	def _prompt_write(self):
		self.user_blog.new_post()
    def _list_blogs(self):
    	blogs=Database.find(collection='blogs',query={})
    	for blog in blogs:
    		print("ID: {},title:{},author:{}".format(blog['idno'],blog['title'],blog['author']))
    def _view_blogs(self):
    	blog_to_see=input("Enter ID of blog you want to view")
    	blogs=blog.from_mongo(blog_to_see)
    	posts=blog.get_posts()
    	for post in posts:
    		print("Date:{},title:{} \n\n{}".format(post['created_date'],post['title'],post['content']))
		