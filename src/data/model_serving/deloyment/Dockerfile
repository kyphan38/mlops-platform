FROM python:3.11-slim as build

# Set up a virtual environment
RUN python -m venv /opt/venv 
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip -r /app/requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]