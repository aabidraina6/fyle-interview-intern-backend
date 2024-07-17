FROM python:3.8

# Set the working directory in the container
WORKDIR /core

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Environment variable to ensure Flask knows where the app is
ENV FLASK_APP=core/server.py


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
