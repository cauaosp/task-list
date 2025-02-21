from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)
print("Database URL:", app.config["SQLALCHEMY_DATABASE_URI"])

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Houve um erro ao adicionar uma nova tarefa: {str(e)}"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Houve um problema para deletar esta tarefa: {str(e)}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Problema ao atualizar tarefa: {str(e)}"
    else:
        return render_template("update.html", task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
