from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True

blogs=[]
db=SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'
class   Blog(db.Model):
        id= db.Column(db.Integer, primary_key= True)
        title= db.Column(db.String(120))
        body= db.Column(db.String(500))
        owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
        def __init__(self,title,body,owner):
            self.title=title
            self.body=body
            self.owner=owner
class   User(db.Model):
        id=db.Column(db.Integer, primary_key= True)
        username=db.Column(db.String(50))
        password=db.Column(db.String(15))
        blogs=db.relationship('Blog', backref='owner')
        
        def __init__(self,username,password):
            self.username=username
            self.password=password
        

@app.before_request
def require_login():
    allowed_routes= ['index','login','signup','blog']
    if  request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
            
@app.route('/login', methods=['POST','GET'])
def login():
    if  request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if  user and user.password==password:
            session['username']=username
            flash('logged in')
            return  redirect('/newpost')
        else:
            flash('User password incorret, or user does not exist', 'error')
    return render_template("login.html")
        


@app.route('/newpost')
def newpost():
    return render_template('new_entry_form.html', title="Create new blog entry")

@app.route('/blog',methods=['GET'])
def display_blog_entries():
    if request.method=='GET':
        if not request.args.get('id') is None:
            entry_id =(int)(request.args.get('id'))
            entry =Blog.query.filter_by(entry_id =entry_id ).first()
            return render_template('single_entry.html', title="Blog Entry", entry=entry)
        if not request.args.get('user') is None:
            entry_id = request.args.get('id')=(int)(request.args.get('user'))
            users=User.query.filter_by(id=id).all()
            all_entries =Blog.query.all()
            return render_template('all_entries.html', title="All Entries", all_entries=all_entries,users=users)
    #entry =Blog.query.all()
        if  not request.args.get('page') is None:
            page=(int)(request.args.get('page'))
        else:
            page=1
        users=User.query.all()  
        all_entries = Blog.query.all()
        return render_template('all_entries.html', title="All Entries", all_entries=all_entries,users=users)
    

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
    
        if username=="" or username==" ":
            flash("That not valid user")
        elif password==""  or password==" " or len(password)<3:
            flash("That's password  not valid")
        elif verify=="" or verify==" ":
            flash("password does not match")
        else:
            existing_user = User.query.filter_by(username=username).first()
        
            if  existing_user:  
                flash('user name already exist','error')
            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
        
    # TODO - user better response messaging
            #return "<h1>User Name already Exist</h1>"

    return render_template('signup.html')
    
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')    

@app.route('/',methods=['POST', 'GET'])
def index():
    #owner = User.query.filter_by(username=session['username']).first()
    
    users = User.query.all()
    return render_template('index.html',title="Blogz Users",users=users)
    

    
@app.route('/newpost',methods=['POST'])
def newpost():  
    owner = User.query.filter_by(username=session['username']).first()
    if request.method=='POST':
        newpost_title = request.form['title']
        newpost_body= request.form['body']
        newpost = Blog(newpost_title, newpost_body, owner=owner)
        if newpost_title=="" or newpost_body=="" or newpost_title==" " or newpost_body==" ":
            flash("invalid")
            return render_template('new_entry_form.html')

        db.session.add(newpost)
        db.session.commit()
        all_entries=Blog.query.order_by("id desc").all()
        return redirect('/blog')
    return render_template('all_entries.html', title="All Entries", all_entries=all_entries)


if __name__=='__main__':
    app.run()