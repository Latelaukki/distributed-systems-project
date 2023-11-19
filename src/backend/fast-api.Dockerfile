FROM python:3.8.10

WORKDIR /src

COPY requirements.txt ./
COPY fast-api.py  ./

RUN pip install -r requirements.txt --progress-bar off

CMD ["uvicorn", "fast-api:app", "--reload", "--host", "0.0.0.0", "--port", "80"]