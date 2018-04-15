from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggin@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'bloggin'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    blog = db.Column(db.String(600))

    def __init__(self, title, blog):
        self.title = title
        self.blog = blog


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    page_title = 'Add a Blog Entry'
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        if title == '' or blog == '':
            flash("You can't post empty fields. Please try again", "error")
            return render_template('new-post.html', page_title=page_title)
        else:
            new_blog = Blog(title, blog)
            db.session.add(new_blog)
            db.session.commit()
            view_post = Blog.query.filter_by(title=title).first()
            blog_id = str(view_post.id)
            return redirect('/blog?id=' + blog_id)        
    return render_template('new-post.html', page_title=page_title)

@app.route('/blog', methods=['GET'])
def index():
    page_title = 'Build a Blog'
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id:
        entry = Blog.query.filter_by(id=blog_id).first()
        return render_template('view-post.html', page_title=entry.title, entry=entry)
    return render_template('blog-home.html', page_title=page_title, blogs=blogs)



if __name__ == '__main__':
    app.run()