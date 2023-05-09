FROM python:3.10.6-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR .
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["./entrypoint.sh"]