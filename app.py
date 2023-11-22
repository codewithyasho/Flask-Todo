from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure MySQL database using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/taskhub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db = SQLAlchemy(app)

# Create a Task model


class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Task(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Task.query.all()
    # print(allTodo)
    return render_template("index.html", allTodo=allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    deltTodo = Task.query.filter_by(sno=sno).first()
    db.session.delete(deltTodo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False, port=5000)
