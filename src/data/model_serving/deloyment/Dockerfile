FROM python:3.11-slim AS build

# Set up a virtual environment
RUN python -m venv /opt/venv 
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip -r /app/requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS final

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . .

# Expose port 7000 for the FastAPI application
EXPOSE 7000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
