from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ljjwqzak:Yk-H8CMwDU7gSOjGxDtediy-YIMQwcOb@snuffleupagus.db.elephantsql.com/ljjwqzak'

# "sqlite:///instance/todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.app_context().push() 

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    
    def formatted_date(self):
        return self.date_created.strftime("%Y-%m-%d %H:%M") #string from time 

    def __str__(self):
        return f"{self.sno} - {self.desc}"
    
@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method =='POST':
        title= request.form["title"]
        desc= request.form["desc"]
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit() 
    #Query all rows
    allTodo= Todo.query.all() 
    return render_template("index.html", allTodo=allTodo)
    
@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title= request.form["title"]
        desc= request.form["desc"]
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo= Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/search', methods=["GET","POST"])
def search():
    search_term = request.form["search"]
    # Query the database to find matching Todo items, case insensitive
    matching_todo = Todo.query.filter(Todo.title.ilike(f"%{search_term}%")).all()
    return render_template("search.html", matching_todo=matching_todo)

if __name__ == "__main__":
    app.run(debug=True)