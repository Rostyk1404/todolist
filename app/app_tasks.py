from flask import Flask, request
from flask_restful import Resource, Api
from models.tasks import Tasks as DB_TASKS

app = Flask(__name__)
api = Api(app)


class Task(Resource):
    def get(self, task_id):
        task = DB_TASKS.get_task_by_id(task_id)
        print(task)
        output_task = {"task_id": task.task_id,
                       "task_name": task.task_name
                       }
        return output_task, 200

    def put(self, task_id):
        body = request.json
        task = DB_TASKS.update_task(task_id, body)
        output_task = {
            "task_name": task.task_name
        }
        return output_task, 200

    def delete(self, task_id):
        DB_TASKS.delete_task(task_id)
        return 204


class Tasks(Resource):
    def get(self):
        list_of_tasks = []
        tasks = DB_TASKS.get_all_tasks()
        for task in tasks:
            output_task = {"task_id": task.task_id,
                           "task_name": task.task_name
                           }
            list_of_tasks.append(output_task)
        return list_of_tasks, 200

    def post(self):
        body = request.json
        task_name = body.get("task_name")
        user_id = body.get("user_id")
        task = DB_TASKS.create_task(task_name, user_id)
        task = DB_TASKS.get_task_by_name(task_name)
        output_task = {"task_id": task.task_id,
                       "task_name": task.task_name,
                       "user_id": task.user_id,
                       }
        return output_task, 200

    def delete(self):
        DB_TASKS.delete_all_task()
        return 204


api.add_resource(Tasks, "/tasks")
api.add_resource(Task, "/tasks/<task_id>")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
