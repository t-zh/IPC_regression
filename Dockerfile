# Base image is Python 3.9
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the model and application code into the container
COPY ./app .
EXPOSE 5000

ENTRYPOINT [ "python", "app.py" ]
