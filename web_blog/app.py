from models.blog import Blog
from models.user import User
from models.post import Post

from database import Database

from flask import Flask, render_template, request, session, make_response, redirect

app = Flask(__name__)
app.secret_key = 'gsds'


@app.route('/')
def home_template():
    if session['email'] is not None:
        return redirect("/profile")
    else:
        return render_template('home.html', email=session['email'])


@app.route('/logout')
def logout():
    User.logout()
    return redirect("/")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session['email'] is not None:
        return redirect('/profile')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.login_valid(email, password):
            User.login(email)
            return redirect('/profile')
    return render_template('login.html')


@app.route('/profile')
def profile():
    return render_template('profile.html', email=session['email'])


@app.route('/register', methods=['POST', 'GET'])
def register_template():
    if session['email'] is not None:
        return redirect('/profile')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        User.register(email, password)
        User.login(email)
        return render_template('profile.html', email=session['email'])
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/blogs/<string:User_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('user_blogs.html', blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        new_blog = Blog(user.email,title,description,user._id)
        new_blog.save_to_mongo()
        return redirect("/blogs")


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])
        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()
        return redirect("/posts/"+blog_id)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.get_from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html', blog_id=blog._id, posts=posts, blog_title=blog.title)


if __name__ == '__main__':
    app.run(port=4995, debug=True)
