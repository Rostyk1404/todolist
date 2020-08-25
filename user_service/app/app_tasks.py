from flask import Flask, request
from flask_restful import Resource, Api
from models.tasks import TaskSchema, Tasks as DB_TASKS

task_app = Flask(__name__)
api = Api(task_app)


class Task(Resource):
    def get(self, task_id):
        task = DB_TASKS.get_task_by_id(task_id)
        print(task)
        task_schema = TaskSchema(only=("task_name", "task_id"))
        output_task = task_schema.dump(task)
        return output_task, 200

    def put(self, task_id):
        body = request.json
        task = DB_TASKS.update_task(task_id, body)
        task_schema = TaskSchema(only=("task_name"))
        output_task = task_schema.dump(task)
        return output_task, 200

    def delete(self, task_id):
        DB_TASKS.delete_task(task_id)
        return 204


class Tasks(Resource):
    def get(self):
        tasks = DB_TASKS.get_all_tasks()
        task_schema = TaskSchema(only=("task_id", "task_name"), many=True)
        output_task = task_schema.dump(tasks)
        return output_task, 200

    def post(self):
        body = request.json
        task_name = body.get("task_name")
        user_id = body.get("user_id")
        task = DB_TASKS.create_task(task_name, user_id)
        # task = DB_TASKS.get_task_by_id(task_id)
        task_schema = TaskSchema(only=("task_id", "task_name", "user_id"))
        output_task = task_schema.dump(task)
        return output_task, 200

    def delete(self):
        DB_TASKS.delete_all_task()
        return 204


api.add_resource(Tasks, "/tasks")
api.add_resource(Task, "/tasks/<task_id>")

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8000)

#
