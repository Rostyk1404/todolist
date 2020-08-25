from app.app import app
from app.app_tasks import task_app
from models.user import Users
from models.tasks import Tasks

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
