# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip3 install -r requirements.txt

# Run my_bot.py when the container launches
CMD ["python", "bot.py"]