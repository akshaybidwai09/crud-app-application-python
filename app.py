from os import error
from flask import Flask, json,render_template,redirect,url_for,request,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mission@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Todo(db.Model):
    __tablename__ = "myapp"
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(),nullable = False)
    completed = db.Column(db.Boolean, nullable=False,
    default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'
#db.create_all()        
@app.route('/myapp/create', methods=['POST'])

def create_todo():
  error =False
  try:
    body = {}
    description = request.get_json()['description']
    id = request.get_json()['']
    todo = Todo(description = description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
    db.session.close() 
  if error:
    abort(400)  
  else:
    return jsonify(body)
#Getting User Data in Flask — Part 2

@app.route('/myapp/<todo_id>/set-completed',methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    #Azax request
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))      

@app.route('/myapp/<todo_id>',methods=['DELETE'])
def delete_item(todo_id):
  try:
    Todo.query.filter_by(id= todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({'success':True})   
@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.order_by('id').all())
    #jinja process a non html in the html process





####################without AJAX##############################
# class Todo(db.Model):
#     __tablename__ = "myapp"
#     id = db.Column(db.Integer,primary_key=True)
#     description = db.Column(db.String(),nullable = False)

#     def __repr__(self):
#         return f'<Todo {self.id} {self.description}>'
# db.create_all()        
# @app.route('/myapp/create', methods=['POST'])
# def create_todo():
#   description = request.form.get('description', '')
#   todo = Todo(description = description)
#   db.session.add(todo)
#   db.session.commit()
# # redirect is important
#   return redirect(url_for('index'))
# #Getting User Data in Flask — Part 2
# @app.route('/')
# def index():
#     return render_template('index.html',data=Todo.query.all())
#     #jinja process a non html in the html process
