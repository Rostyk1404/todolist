FROM python:3.8.2
COPY /user_service/ user_service
#COPY /requirements.txt /requirements.txt
WORKDIR user_service
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "run.py"]
