# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

# Run app.py when the container launches
CMD ["python", "bot.py"]
#CMD ["sh", "-c", "while true; do sleep 60; done"]
