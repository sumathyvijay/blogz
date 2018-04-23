from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO']=True

blogs=[]
db=SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'
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
def newpost():  
    owner = User.query.filter_by(username=session['username']).first()
    if  request.method=='POST':
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