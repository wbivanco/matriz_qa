# Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster

# # Set the working directory in the container to /app
# WORKDIR /app

# # Add the current directory contents into the container at /app
# ADD . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Run app.py when the container launches
# CMD ["python", "app.py"]



FROM python:3.9-slim

#ENV FLASK_APP="flask_main.py"

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]