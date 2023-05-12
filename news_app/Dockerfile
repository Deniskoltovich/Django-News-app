FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR .
RUN apt-get update \
    && apt-get install gcc libpq-dev python3-dev \
    --no-install-recommends -y
COPY requirements.txt .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["./entrypoint.sh"]