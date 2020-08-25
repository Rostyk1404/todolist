FROM python:3.8.2
COPY /user_service /user_service
WORKDIR user_service
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "models/user.py"]
CMD ["python", "run.py"]
