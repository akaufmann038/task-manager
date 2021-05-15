from types import MethodType
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

class task:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def update_content(self, new_content):
        self.content = new_content

class database:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, content):
        self.tasks.append(task(len(self.tasks), content))

    def get_tasks(self):
        return self.tasks

    def get_task(self, id):
        for task in self.tasks:
            if task.id == int(id):
                return task

    def update_task(self, id, content):
        for task in self.tasks:
            if task.id == int(id):
                task.update_content(content)

    def remove_task(self, id):
        new_tasks = []
        for task in self.tasks:
            if task.id != int(id):
                new_tasks.append(task)

        self.tasks = new_tasks

database = database()




@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        task_text = request.form["new-task"]

        # add task to data
        database.add_task(task_text)

        return render_template("tasks.html", task_content=database.get_tasks())
    else:
        return render_template("tasks.html", task_content=database.get_tasks())

@app.route("/delete/<task_id>", methods=["GET"])
def delete(task_id):
    # remove task from tasks
    database.remove_task(task_id)
    
    return redirect(url_for("home"))

@app.route("/update/<task_id>", methods=["GET", "POST"])
def update(task_id):
    if request.method == "GET":
        return render_template("update.html", task_id=task_id, task=database.get_task(task_id))
    else:
        # update task
        new_content = request.form["update-task"]
        database.update_task(task_id, new_content)

        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)