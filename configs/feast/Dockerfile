FROM python:3.10-slim

ENV FEAST_USAGE=False
ENV FEAST_TELEMETRY=False

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["feast", "apply"]
