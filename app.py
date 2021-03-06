from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	complete = db.Column(db.Boolean)


@app.route('/')
def home():
	todo_list = Todo.query.all()
	return render_template('list.html', todo_list=todo_list)


@app.route('/add', methods=["POST"])
def add():
	title = request.form.get("title")
	new_todo_list = Todo(title=title,complete=False)
	db.session.add(new_todo_list)
	db.session.commit()
	return redirect(url_for('home'))


@app.route('/edit/<int:todo_id>')
def edit(todo_id):
	todo = Todo.query.filter_by(id=todo_id).first() 
	print(todo.complete)
	todo.complete =  not todo.complete
	db.session.commit()
	return redirect(url_for('home'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
	todo = Todo.query.filter_by(id=todo_id).first() 
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('home'))


if __name__ == '__main__':
	db.create_all()
	app.run()