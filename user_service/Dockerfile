FROM python:3.8.2
WORKDIR /user_service
COPY /user_service /user_service
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "run.py"]
