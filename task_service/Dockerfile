FROM python:3.8.2
COPY /task_service /task_service
#COPY /requirements.txt /requirements.txt
WORKDIR task_serice
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "app_tasks.py"]
