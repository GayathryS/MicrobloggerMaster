import users
import blog
from flask import Flask,render_template,request,session
app=Flask(__name__)
app.secret_key="gsds"

@app.route('/')
def home_template():
	return render_template('home.html')

@app.route('/login')
def login_template():
	return render_template('login.html')

@app.route('/register')
def register_template():
	return render_template('register.html')

@app.before_first_request
def initialize_database():
	database.initialize()

@app.route('/auth/login',methods=['POST'])
def login_user():
	email=request.form['email']
	password=request.form['password']
	if user.login_valid(email,password):
		user.login(email)
	else:
	  	session['email']=None
	return render_template("profile.html",email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
	email=request.form['email']
	password=request.form['password']
	user.register(email,password)
	session['email']=email

	return render_template("profile.html",email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
	if user_id is not None:
		user=user.get_by_id(user_id)
	else:
		user=user.get_by_email(session['email'])
	blogs=user.get_blogs()
    return render_template("user_blogs.html",blogs=blogs)

@app.route('/blogs/new',methods=['POST','GET'])
def create_new_blog():
	if request,method=='GET':
		return render_template('new_blog,html')
	else:
		title=request.form['title']
		description=request.form['description']
		user=user.get_by_email(session['email'])
		new_blog=blog(user.email,title,description,user.idno)
		new_blog.save_to_mongo()
		return make_response(user_blogs(user.idno))

@app.route('/posts/new/<string:blog_id>',methods=['POST','GET'])
def create_new_post():
	if request,method=='GET':
		return render_template('new_post,html')
	else:
		title=request.form['title']
		content=request.form['content']
		user=user.get_by_email(session['email'])
		new_post=post(blog_id,title,content,user.email)
		new_post.save_to_mongo()
		return make_response(user_blogs(user.idno))

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
	blog=blog.from_mongo(blog_id)
	posts=blog.get_posts()
	return render_template('posts.html',posts=posts,blog_title=blog.title)

if __name__ =='__main__':
	app.run(port=4995)