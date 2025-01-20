# Pull the official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the application code
COPY . /code/

# Use Gunicorn to serve the application
CMD ["gunicorn", "employee-management.wsgi:application", "--bind", "0.0.0.0:8000"]
