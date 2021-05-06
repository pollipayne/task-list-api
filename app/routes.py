from flask import Blueprint
from app.models.task import Task
from flask import Blueprint, make_response, jsonify, request
from app import db
from sqlalchemy import asc, desc



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def task_checker(request_body, task):
    # so everything should default to is_complete false but i will need some sort of a check on the completed_at variable to determine when to switch that to true. 
        
    pass
        



@task_bp.route("", methods=["GET", "POST"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    if request.method == "GET":
        task_response = []

        for task in tasks:
            task_response.append({"id": task.task_id, 
                                "title": task.title, 
                                "description": task.description, 
                                "is_complete": False})
        return jsonify(task_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)
        db.session.add(new_task)
        db.session.commit()

        return make_response({"task": new_task.to_json()}, 201)

@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def get_single_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"task": task.to_json()}
    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]

        db.session.commit()

        return make_response({"task": task.to_json()}, 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

